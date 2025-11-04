import qrcode
import qrcode.image.svg
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET

def generate_svg_qr_with_icon(url, icon_path, output_filename="qr_with_icon.svg", box_size=10, border=4, error_correction=ERROR_CORRECT_H):
    """
    URLをエンコードしたSVG形式のQRコードの中央にSVGアイコンを埋め込みます。

    Args:
        url (str): QRコードにエンコードするURL。
        icon_path (str): 中央に埋め込むSVGアイコンのファイルパス。
        output_filename (str): 生成されるQRコード画像のファイル名（SVG形式）。
        box_size (int): QRコードの各ボックスのピクセルサイズ。
        border (int): QRコードの周囲のボーダーサイズ。
        error_correction (int): エラー訂正レベル。
                             アイコン埋め込みには、H (最高: 約30%の破損まで復元可能) を推奨。
    """
    try:
        # 1. SVG形式のQRコードを生成
        factory = qrcode.image.svg.SvgPathImage
        qr = qrcode.QRCode(
            version=None,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
            image_factory=factory,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # QRコード画像をSVGとして生成
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # SVGを文字列として取得
        import io
        svg_buffer = io.BytesIO()
        qr_img.save(svg_buffer)
        svg_buffer.seek(0)
        qr_svg_content = svg_buffer.read().decode('utf-8')

        # 2. QRコードのSVGをパース
        qr_root = ET.fromstring(qr_svg_content)

        # 名前空間を取得
        ns = {'svg': 'http://www.w3.org/2000/svg'}
        if qr_root.tag.startswith('{'):
            ns_url = qr_root.tag[1:qr_root.tag.index('}')]
            ns = {'svg': ns_url}

        # QRコードのサイズを取得
        qr_width = float(qr_root.get('width', '100').replace('mm', ''))
        qr_height = float(qr_root.get('height', '100').replace('mm', ''))

        # 3. SVGアイコンを読み込み
        with open(icon_path, 'r', encoding='utf-8') as f:
            icon_svg_content = f.read()

        icon_root = ET.fromstring(icon_svg_content)

        # アイコンのサイズを取得（viewBoxまたはwidth/heightから）
        viewbox = icon_root.get('viewBox')
        if viewbox:
            vb_parts = viewbox.split()
            vb_x, vb_y, icon_width, icon_height = map(float, vb_parts)
        else:
            vb_x, vb_y = 0, 0
            icon_width = float(icon_root.get('width', '100').replace('px', '').replace('mm', ''))
            icon_height = float(icon_root.get('height', '100').replace('px', '').replace('mm', ''))

        # 4. アイコンをQRコードの中央に配置するためのグループを作成
        # アイコンのサイズをQRコードの約20%に設定
        icon_scale = (qr_width / 4) / max(icon_width, icon_height)

        # QRコードとアイコンの中心座標を計算
        qr_center_x = qr_width / 2
        qr_center_y = qr_height / 2
        icon_center_x = vb_x + icon_width / 2
        icon_center_y = vb_y + icon_height / 2

        # アイコン用のグループを作成
        icon_group = ET.Element('g', {
            'transform': f'translate({qr_center_x}, {qr_center_y})'
        })

        # アイコンの背景用の白い円を追加（アイコンより少し大きく）
        background_radius = max(icon_width, icon_height) * icon_scale * 0.7
        background_circle = ET.Element('circle', {
            'cx': '0',
            'cy': '0',
            'r': str(background_radius),
            'fill': 'white'
        })
        icon_group.append(background_circle)

        # アイコン要素用のグループ
        g = ET.Element('g', {
            'transform': f'scale({icon_scale}) translate({-icon_center_x}, {-icon_center_y})'
        })

        # アイコンの全ての子要素をグループにコピー
        for child in icon_root:
            g.append(child)

        # アイコンを背景の上に配置
        icon_group.append(g)

        # QRコードSVGにアイコングループを追加
        qr_root.append(icon_group)

        # 5. 最終的なSVGを保存
        tree = ET.ElementTree(qr_root)
        ET.register_namespace('', ns.get('svg', 'http://www.w3.org/2000/svg'))
        tree.write(output_filename, encoding='utf-8', xml_declaration=True)

        print(f"✅ SVGアイコン付きQRコードを '{output_filename}' に保存しました。")

    except FileNotFoundError:
        print(f"❌ エラー: アイコンファイルが見つかりません: {icon_path}")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()


def generate_qr_with_icon(url, icon_path, output_filename="qr_with_icon.png", box_size=10, border=4, error_correction=ERROR_CORRECT_H):
    """
    URLをエンコードしたQRコードの中央にアイコン画像を埋め込みます。

    Args:
        url (str): QRコードにエンコードするURL。
        icon_path (str): 中央に埋め込むアイコン画像のファイルパス。
        output_filename (str): 生成されるQRコード画像のファイル名。
        box_size (int): QRコードの各ボックスのピクセルサイズ。
        border (int): QRコードの周囲のボーダーサイズ。
        error_correction (int): エラー訂正レベル。
                             アイコン埋め込みには、H (最高: 約30%の破損まで復元可能) を推奨。
    """
    try:
        # 1. QRコードの生成
        qr = qrcode.QRCode(
            version=None,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # QRコード画像をPIL Imageオブジェクトとして作成
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        
        # 2. アイコン画像の読み込みとリサイズ
        icon = Image.open(icon_path).convert("RGBA")
        
        # アイコンをQRコードサイズに対して適切なサイズにリサイズ
        # 例：QRコードサイズの約20%に収まるようにする
        qr_width, qr_height = qr_img.size
        icon_max_size = int(qr_width / 6) # QRコード幅の1/5
        
        # アスペクト比を維持してリサイズ
        icon.thumbnail((icon_max_size, icon_max_size))
        
        icon_width, icon_height = icon.size
        
        # 3. アイコンをQRコードの中央に配置
        # 配置座標を計算
        x = (qr_width - icon_width) // 2
        y = (qr_height - icon_height) // 2
        
        # QRコード画像にアイコンを貼り付け（アルファチャンネルを考慮してマスクを使用）
        # アイコンの形状が円形や角丸であっても対応できるようにするため
        qr_img.paste(icon, (x, y), icon)
        
        # 4. 画像の保存
        qr_img.save(output_filename)
        print(f"✅ アイコン付きQRコードを '{output_filename}' に保存しました。")

    except FileNotFoundError:
        print(f"❌ エラー: アイコン画像ファイルが見つかりません: {icon_path}")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")

# --- 💡 使用例 ---
if __name__ == '__main__':
    TARGET_URL = "https://modeltimetable-654704602397.asia-northeast2.run.app/"
    ICON_FILE = "./src/static/images/icon.svg"  # SVGアイコンファイルのパス

    # SVG形式のQRコードを生成
    generate_svg_qr_with_icon(
        url=TARGET_URL,
        icon_path=ICON_FILE,
        border=0,
        output_filename="docs/QR.svg",
        error_correction=ERROR_CORRECT_H  # アイコン埋め込みに必須
    )

    # PNG形式のQRコードを生成する場合は以下を使用
    # generate_qr_with_icon(
    #     url=TARGET_URL,
    #     icon_path="./src/static/images/icon.png",  # PNGアイコンファイルのパス
    #     output_filename="QR.png",
    #     error_correction=ERROR_CORRECT_H
    # )
