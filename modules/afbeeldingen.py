import streamlit as st
from PIL import Image
import io
import numpy as np
import base64
import os

# Canvas specificaties
CANVAS_W = 1024
CANVAS_H = 1536
PRODUCT_H = 720
TOP_MARGIN = 360
SHADOW_PADDING = 30


# ─── Helpers ────────────────────────────────────────────────────────────────

def image_to_bytes(image: Image.Image, fmt: str = "PNG") -> bytes:
    buf = io.BytesIO()
    save_kwargs = {"format": fmt}
    if fmt == "JPEG":
        save_kwargs["quality"] = 95
        if image.mode == "RGBA":
            image = image.convert("RGB")
    image.save(buf, **save_kwargs)
    return buf.getvalue()


def image_to_base64(image: Image.Image) -> str:
    buf = io.BytesIO()
    img = image.convert("RGB") if image.mode == "RGBA" else image
    img.save(buf, format="PNG")
    return base64.standard_b64encode(buf.getvalue()).decode()


def detect_content_bbox(image: Image.Image, white_threshold: int = 238) -> tuple:
    """Bounding box van niet-witte / niet-transparante pixels."""
    arr = np.array(image.convert("RGBA"))
    alpha = arr[:, :, 3]
    has_transparency = (alpha < 255).any()

    if has_transparency:
        mask = alpha > 10
    else:
        rgb = arr[:, :, :3]
        mask = ~(np.all(rgb >= white_threshold, axis=2))

    if not mask.any():
        return (0, 0, image.width, image.height)

    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    rmin, rmax = int(np.where(rows)[0][0]), int(np.where(rows)[0][-1])
    cmin, cmax = int(np.where(cols)[0][0]), int(np.where(cols)[0][-1])
    return (cmin, rmin, cmax + 1, rmax + 1)


# ─── Canvas Transform ────────────────────────────────────────────────────────

def canvas_transform(image: Image.Image) -> Image.Image:
    """
    Plaatst het product op het FRED canvas:
      Canvas : 1024 × 1536 px, achtergrond #FFFFFF
      Product: hoogte 720 px, horizontaal gecentreerd, top margin 360 px
      Schaduw: behouden via padding rondom bounding box
    """
    rgba = image.convert("RGBA")
    cmin, rmin, cmax, rmax = detect_content_bbox(rgba)

    # Schaduw-padding
    cmin = max(0, cmin - SHADOW_PADDING)
    rmin = max(0, rmin - SHADOW_PADDING)
    cmax = min(rgba.width, cmax + SHADOW_PADDING)
    rmax = min(rgba.height, rmax + SHADOW_PADDING)

    product = rgba.crop((cmin, rmin, cmax, rmax))

    # Schaal naar producthoogte 720 px
    w, h = product.size
    new_h = PRODUCT_H
    new_w = int(w * new_h / h)

    # Voorkom uitloop buiten canvas-breedte
    if new_w > CANVAS_W:
        new_w = CANVAS_W
        new_h = int(h * new_w / w)

    product = product.resize((new_w, new_h), Image.LANCZOS)

    # Wit canvas
    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (255, 255, 255, 255))
    x = (CANVAS_W - new_w) // 2
    canvas.paste(product, (x, TOP_MARGIN), product)

    return canvas.convert("RGB")


# ─── Claude analyse ──────────────────────────────────────────────────────────

def _claude_client(api_key: str):
    import anthropic
    return anthropic.Anthropic(api_key=api_key)


def analyze_for_superrealistic(api_key: str, image: Image.Image) -> str:
    """Claude analyseert de afbeelding en geeft een gedetailleerde img2img-prompt terug."""
    client = _claude_client(api_key)
    img_b64 = image_to_base64(image)

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=600,
        thinking={"type": "adaptive"},
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/png", "data": img_b64},
                },
                {
                    "type": "text",
                    "text": (
                        "Analyseer dit productafbeelding zorgvuldig. "
                        "Genereer een gedetailleerde Engelse img2img-prompt voor een superrealistische "
                        "professionele productfoto. Beschrijf het product exact: materiaal, kleur, textuur, "
                        "afmetingen, details. Voeg toe: studio lighting, photorealistic, 8k resolution, "
                        "sharp focus, white seamless background, professional product photography. "
                        "Geef ALLEEN de prompt terug, geen uitleg of opmaak."
                    ),
                },
            ],
        }],
    )
    # Filter ThinkingBlock — alleen de tekst teruggeven
    for block in response.content:
        if block.type == "text":
            return block.text.strip()
    return "photorealistic product on white background, professional studio lighting, 8k, sharp focus"


def analyze_for_variant(
    api_key: str,
    base_image: Image.Image,
    ref_image: Image.Image,
    change_type: str,
    extra: str = "",
) -> str:
    """Claude analyseert basismodel + referentie en geeft een variant-prompt terug."""
    client = _claude_client(api_key)
    base_b64 = image_to_base64(base_image)
    ref_b64 = image_to_base64(ref_image)

    extra_line = f"\nExtra specificatie van de gebruiker: {extra}" if extra else ""
    change_line = f"Gewenste wijziging: {change_type}."

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=700,
        thinking={"type": "adaptive"},
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/png", "data": base_b64},
                },
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/png", "data": ref_b64},
                },
                {
                    "type": "text",
                    "text": (
                        f"Afbeelding 1 = het basismodel product. "
                        f"Afbeelding 2 = de referentie voor de gewenste stijl/kleur/materiaal.\n"
                        f"{change_line}{extra_line}\n\n"
                        "Genereer een Engelse img2img-prompt die:\n"
                        "- De VORM en STRUCTUUR van het basismodel behoudt\n"
                        "- De kleur/materiaal/stoffering overneemt van de referentie\n"
                        "- Eindigt met: professional product photography, studio lighting, "
                        "photorealistic, white background, same product structure as original\n\n"
                        "Geef ALLEEN de prompt terug, geen uitleg."
                    ),
                },
            ],
        }],
    )
    for block in response.content:
        if block.type == "text":
            return block.text.strip()
    return "product with different upholstery, professional product photography, studio lighting, white background"


# ─── Hugging Face img2img ────────────────────────────────────────────────────

def hf_img2img(hf_token: str, image: Image.Image, prompt: str, strength: float = 0.55) -> Image.Image:
    """Stuurt de afbeelding via HuggingFace Inference API door SDXL img2img."""
    from huggingface_hub import InferenceClient

    client = InferenceClient(token=hf_token)

    # Schaal afbeelding voor HF API (max 1024px op langste zijde)
    img_rgb = image.convert("RGB")
    max_dim = 1024
    if max(img_rgb.size) > max_dim:
        ratio = max_dim / max(img_rgb.size)
        img_rgb = img_rgb.resize(
            (int(img_rgb.width * ratio), int(img_rgb.height * ratio)),
            Image.LANCZOS,
        )

    buf = io.BytesIO()
    img_rgb.save(buf, format="PNG")
    buf.seek(0)

    result: Image.Image = client.image_to_image(
        image=buf,
        prompt=prompt,
        model="stabilityai/stable-diffusion-xl-refiner-1.0",
        strength=strength,
    )
    return result


# ─── Streamlit UI ────────────────────────────────────────────────────────────

def _download_row(image: Image.Image, prefix: str):
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "⬇️ Download PNG",
            data=image_to_bytes(image, "PNG"),
            file_name=f"{prefix}.png",
            mime="image/png",
        )
    with col2:
        st.download_button(
            "⬇️ Download JPG",
            data=image_to_bytes(image, "JPEG"),
            file_name=f"{prefix}.jpg",
            mime="image/jpeg",
        )


def show():
    st.title("Afbeeldingsgenerator — FRED")
    st.caption(
        "Verwerk productfoto's naar het FRED canvas-formaat (1024 × 1536 px). "
        "Optioneel: superrealistische bewerking of variant met andere stof / kleur via AI."
    )

    # ── Zijbalk: API-sleutels ─────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("---")
        st.subheader("API-instellingen")
        claude_key = st.text_input(
            "Anthropic API Key",
            type="password",
            value=os.environ.get("ANTHROPIC_API_KEY", ""),
            help="Vereist voor AI-analyse (tabs 2 en 3)",
        )
        hf_token = st.text_input(
            "Hugging Face Token",
            type="password",
            value=os.environ.get("HF_TOKEN", ""),
            help="Gratis token via huggingface.co — vereist voor AI-beeldgeneratie",
        )
        ai_ready = bool(claude_key and hf_token)
        if ai_ready:
            st.success("AI-functies beschikbaar")
        else:
            st.info("Vul beide sleutels in voor AI-tabs")

    # ── Tabs ─────────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(
        ["📐 Canvas Transform", "✨ Superrealistisch", "🎨 Variant aanmaken"]
    )

    # ============================
    # TAB 1 — Canvas Transform
    # ============================
    with tab1:
        st.subheader("Canvas Transformatie")
        st.info(
            "Plaatst het product op het standaard FRED-canvas. "
            "Volledig gratis — geen AI nodig."
        )

        with st.expander("Canvas specificaties", expanded=False):
            st.markdown(
                "| Parameter | Waarde |\n"
                "|---|---|\n"
                "| Canvas | 1024 × 1536 px |\n"
                "| Achtergrond | #FFFFFF |\n"
                "| Producthoogte | 720 px |\n"
                "| Top margin | 360 px |\n"
                "| Uitlijning | Horizontaal gecentreerd |\n"
                "| Schaduw | Behouden |"
            )

        upload1 = st.file_uploader(
            "Upload productafbeelding (PNG of JPG)",
            type=["png", "jpg", "jpeg"],
            key="tab1_upload",
        )

        if upload1:
            img1 = Image.open(upload1)
            col_l, col_r = st.columns(2)
            with col_l:
                st.markdown("**Origineel**")
                st.image(img1, use_column_width=True)
                st.caption(f"{img1.width} × {img1.height} px | {upload1.type}")

            if st.button("Genereer canvas-output", key="tab1_btn", type="primary"):
                with st.spinner("Transformatie uitvoeren…"):
                    result1 = canvas_transform(img1)

                with col_r:
                    st.markdown("**Resultaat (1024 × 1536)**")
                    st.image(result1, use_column_width=True)
                    st.caption(f"{result1.width} × {result1.height} px")

                st.markdown("---")
                _download_row(result1, "fred_canvas")

    # ============================
    # TAB 2 — Superrealistisch
    # ============================
    with tab2:
        st.subheader("Superrealistische productfoto")
        st.info(
            "Claude analyseert de afbeelding en genereert een gedetailleerde prompt. "
            "Hugging Face (SDXL) maakt de superrealistische versie. "
            "Daarna wordt het canvas-formaat automatisch toegepast."
        )

        if not ai_ready:
            st.warning("Vul de API-sleutels in via de zijbalk.")

        upload2 = st.file_uploader(
            "Upload productafbeelding",
            type=["png", "jpg", "jpeg"],
            key="tab2_upload",
            disabled=not ai_ready,
        )
        strength2 = st.slider(
            "AI-intensiteit",
            min_value=0.20,
            max_value=0.85,
            value=0.55,
            step=0.05,
            help="Lager = dichter bij het origineel | Hoger = meer AI-transformatie",
            key="tab2_strength",
        )

        if upload2 and ai_ready:
            img2 = Image.open(upload2)
            st.image(img2, caption="Origineel", width=300)

            if st.button("Genereer superrealistische versie", key="tab2_btn", type="primary"):
                prompt2 = None
                with st.spinner("Stap 1/3 — Claude analyseert de afbeelding…"):
                    try:
                        prompt2 = analyze_for_superrealistic(claude_key, img2)
                        with st.expander("Gegenereerde prompt (klik om te zien)"):
                            st.code(prompt2)
                    except Exception as e:
                        st.error(f"Claude API fout: {e}")
                        st.stop()

                result2_raw = None
                with st.spinner("Stap 2/3 — Hugging Face genereert de afbeelding… (30–90 sec)"):
                    try:
                        result2_raw = hf_img2img(hf_token, img2, prompt2, strength=strength2)
                    except Exception as e:
                        st.error(f"Hugging Face API fout: {e}")
                        st.stop()

                with st.spinner("Stap 3/3 — Canvas transformatie toepassen…"):
                    result2 = canvas_transform(result2_raw)

                st.markdown("---")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.image(img2, caption="Origineel")
                with col_b:
                    st.image(result2, caption="Superrealistisch + FRED canvas")
                _download_row(result2, "fred_superrealistisch")

    # ============================
    # TAB 3 — Variant aanmaken
    # ============================
    with tab3:
        st.subheader("Variant aanmaken")
        st.info(
            "Upload het basismodel én een referentieafbeelding (nieuwe stof of kleur). "
            "Claude begrijpt beide afbeeldingen en stuurt Hugging Face aan om de variant te genereren."
        )

        if not ai_ready:
            st.warning("Vul de API-sleutels in via de zijbalk.")

        col_b, col_r = st.columns(2)
        with col_b:
            upload_base = st.file_uploader(
                "Basismodel (origineel product)",
                type=["png", "jpg", "jpeg"],
                key="tab3_base",
                disabled=not ai_ready,
            )
        with col_r:
            upload_ref = st.file_uploader(
                "Referentie (nieuwe stof / nieuw kleur)",
                type=["png", "jpg", "jpeg"],
                key="tab3_ref",
                disabled=not ai_ready,
            )

        change_type3 = st.radio(
            "Type wijziging",
            ["Stoffering / bekleding", "Kleur onderstel / frame", "Beide"],
            horizontal=True,
            key="tab3_change",
        )
        extra3 = st.text_input(
            "Extra omschrijving (optioneel)",
            placeholder="bijv. 'verander alleen het onderstel naar mat zwart'",
            key="tab3_extra",
        )
        strength3 = st.slider(
            "AI-intensiteit",
            min_value=0.30,
            max_value=0.85,
            value=0.60,
            step=0.05,
            key="tab3_strength",
        )

        if upload_base and upload_ref and ai_ready:
            img_base = Image.open(upload_base)
            img_ref = Image.open(upload_ref)

            col_pb, col_pr = st.columns(2)
            with col_pb:
                st.image(img_base, caption="Basismodel", use_column_width=True)
            with col_pr:
                st.image(img_ref, caption="Referentie", use_column_width=True)

            if st.button("Genereer variant", key="tab3_btn", type="primary"):
                prompt3 = None
                with st.spinner("Stap 1/3 — Claude analyseert beide afbeeldingen…"):
                    try:
                        prompt3 = analyze_for_variant(
                            claude_key, img_base, img_ref,
                            change_type=change_type3,
                            extra=extra3,
                        )
                        with st.expander("Gegenereerde prompt (klik om te zien)"):
                            st.code(prompt3)
                    except Exception as e:
                        st.error(f"Claude API fout: {e}")
                        st.stop()

                result3_raw = None
                with st.spinner("Stap 2/3 — Hugging Face genereert de variant… (30–90 sec)"):
                    try:
                        result3_raw = hf_img2img(hf_token, img_base, prompt3, strength=strength3)
                    except Exception as e:
                        st.error(f"Hugging Face API fout: {e}")
                        st.stop()

                with st.spinner("Stap 3/3 — Canvas transformatie toepassen…"):
                    result3 = canvas_transform(result3_raw)

                st.markdown("---")
                col_r1, col_r2, col_r3 = st.columns(3)
                with col_r1:
                    st.image(img_base, caption="Basismodel")
                with col_r2:
                    st.image(img_ref, caption="Referentie")
                with col_r3:
                    st.image(result3, caption="Gegenereerde variant")
                _download_row(result3, "fred_variant")
