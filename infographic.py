import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox, HPacker, VPacker, TextArea
from matplotlib.patches import FancyBboxPatch
from matplotlib import patheffects
from pathlib import Path
import numpy as np
from PIL import Image

# Папка с изображениями
IMG_DIR = Path("img")

def save_final_image(path: Path):
    with Image.open(path) as im:
        rgb_im = im.convert("RGB")
        max_size = (1280, 1280)
        rgb_im.thumbnail(max_size, Image.LANCZOS)
        jpg_path = path.with_suffix(".jpg")
        rgb_im.save(jpg_path, format="JPEG", quality=95)
    return jpg_path

def generate_gradient_color(y, height):
    t = y / height
    gray = 1.0 - 0.1 * t
    return (gray, gray, gray)

def generate_infographic(price, stats, logo_path=IMG_DIR / "logo.png", icon_path=IMG_DIR / "fon.png"):
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    gradient = np.linspace(0.95, 0.2, 100).reshape(-1, 1)
    ax.imshow(gradient, extent=[0, 1, 0, 1], cmap="Greys", aspect="auto", zorder=0)
    ax.axis("off")

    title_y = 0.92
    center_x = 0.5
    spacing = 0.04
    ax.text(center_x - spacing * 1.5, title_y, "Mining", ha="right", va="center",
            fontsize=24, weight="bold", color="white", zorder=4)

    try:
        img = mpimg.imread(logo_path)
        zoom = 40 / img.shape[0]
        imagebox = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(imagebox, (center_x, title_y), frameon=False, box_alignment=(0.5, 0.5), zorder=5)
        ax.add_artist(ab)
    except Exception as e:
        print(f"Error loading logo image: {e}")

    ax.text(center_x + spacing * 1.5, title_y, "Hash", ha="left", va="center",
            fontsize=24, weight="bold", color="white", zorder=4)

    total_width = 0.85
    margin_side = (1 - total_width) / 2
    cols = 2
    rows = 2
    cell_width = total_width / cols
    cell_height = 0.09
    gap_x = 0.055
    gap_y = 0.06
    xs = [margin_side + i * cell_width for i in range(cols)]
    start_y = title_y - 0.13
    ys = [start_y - i * (cell_height + gap_y) for i in range(rows)]

    top_cells = [
        {"pos": (xs[0], ys[0]), "text": f"Price:\n${price:.8f}"},
        {"pos": (xs[1], ys[0]), "text": f"Liquidity:\n${stats['reserve_usd']:,.0f}"},
        {"pos": (xs[0], ys[1]), "text": f"Volume 24h:\n${stats['volume_24h']:,.0f}"},
        {"pos": (xs[1], ys[1]), "text": f"FDV:\n${stats['fdv_usd']:,.0f}"},
    ]

    try:
        icon_img = mpimg.imread(icon_path)
        icon_zoom = 12 / icon_img.shape[0]
        icon = OffsetImage(icon_img, zoom=icon_zoom)
    except Exception as e:
        print(f"Error loading icon image: {e}")
        icon = None

    for cell in top_cells:
        x, y = cell["pos"]
        gradient_color = generate_gradient_color(1 - y, 1)
        ax.add_patch(FancyBboxPatch(
            (x + gap_x / 2, y - cell_height - gap_y / 2),
            cell_width - gap_x, cell_height,
            boxstyle="round,pad=0.015",
            linewidth=0.4,
            edgecolor="#444",
            facecolor=gradient_color,
            zorder=3,
            path_effects=[patheffects.withSimplePatchShadow(offset=(1.2, -1.2), alpha=0.25)]
        ))

        text_area = TextArea(cell["text"], textprops=dict(color="black", fontsize=14, weight="semibold"))
        if icon:
            box = HPacker(children=[icon, text_area], align="center", pad=0, sep=6)
        else:
            box = text_area

        ab = AnnotationBbox(
            box,
            (x + cell_width / 2, y - cell_height / 2 - gap_y / 2),
            frameon=False,
            box_alignment=(0.5, 0.5),
            zorder=4
        )
        ax.add_artist(ab)

    # --- Нижние NFT ячейки ---
    footer_y = ys[-1] - 0.2
    footer_bottom_y = 0.05
    footer_height_new = footer_y - footer_bottom_y

    nft_width = 0.44
    gap_between = 0.05
    total_width = 2 * nft_width + gap_between
    left_margin = (1 - total_width) / 2
    nft1_x = left_margin
    nft2_x = nft1_x + nft_width + gap_between
    gap_y = 0.02

    def add_nft_block(x, title, subtitle, image_file):
        gradient_color = generate_gradient_color(1 - footer_y, 1)
        ax.add_patch(FancyBboxPatch(
            (x, footer_bottom_y + gap_y),
            nft_width, footer_height_new - 2 * gap_y,
            boxstyle="round,pad=0.015",
            linewidth=0.4,
            edgecolor="#444",
            facecolor=gradient_color,
            zorder=3,
            path_effects=[patheffects.withSimplePatchShadow(offset=(1.2, -1.2), alpha=0.25)]
        ))

        try:
            img = mpimg.imread(IMG_DIR / image_file)
            zoom = (footer_height_new - 2 * gap_y) * 300 / img.shape[0] * 0.8
            imagebox = OffsetImage(img, zoom=zoom)

            title_text = TextArea(title, textprops=dict(color="black", fontsize=14, weight="bold"))
            subtitle_text = TextArea(subtitle, textprops=dict(color="black", fontsize=12))
            text_box = VPacker(children=[title_text, subtitle_text], align="left", pad=0, sep=2)
            full_box = HPacker(children=[imagebox, text_box], align="center", pad=0, sep=8)

            ab = AnnotationBbox(
                full_box,
                (x + nft_width / 2, footer_bottom_y + footer_height_new / 2),
                frameon=False,
                box_alignment=(0.5, 0.5),
                zorder=4
            )
            ax.add_artist(ab)
        except Exception as e:
            print(f"Error loading {image_file}: {e}")
            ax.text(
                x + nft_width / 2, footer_bottom_y + footer_height_new / 2,
                f"{title}\n{subtitle}",
                ha="center", va="center",
                fontsize=16, color="black", weight="bold", zorder=4
            )

    add_nft_block(nft1_x, "Inventory", "Asic miner", "asic.png")
    add_nft_block(nft2_x, "Plasma Cat", "NFT collision", "plasma.png")

    path = Path("info_tmp.png")
    plt.savefig(path, bbox_inches=None, pad_inches=0, transparent=False)
    plt.close()

    final_path = save_final_image(path)
    path.unlink(missing_ok=True)
    return final_path.resolve()
