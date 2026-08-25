import cv2
from flask import Flask, Response

app = Flask(__name__)

camera = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)

camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_FPS, 30)


def generate_frames():
    while True:
        success, frame = camera.read()

        if not success:
            continue

        success, buffer = cv2.imencode(
            ".jpg",
            frame,
            [cv2.IMWRITE_JPEG_QUALITY, 80]
        )

        if not success:
            continue

        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes
            + b"\r\n"
        )


@app.route("/stream")
def stream():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/")
def index():
    return """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>MantisCV</title>

    <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;

            background: #0d1117;
            color: #e6edf3;

            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
        }

        .container {
            width: min(1100px, 94%);
            margin: 0 auto;
            padding: 32px 0;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;

            margin-bottom: 24px;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .logo {
            width: 42px;
            height: 42px;

            display: flex;
            align-items: center;
            justify-content: center;

            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 10px;

            font-size: 22px;
        }

        h1 {
            margin: 0;
            font-size: 24px;
            font-weight: 600;
            letter-spacing: -0.5px;
        }

        .subtitle {
            margin-top: 3px;

            color: #8b949e;
            font-size: 13px;
        }

        .status {
            display: flex;
            align-items: center;
            gap: 8px;

            padding: 8px 12px;

            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 20px;

            font-size: 13px;
            color: #8b949e;
        }

        .status-dot {
            width: 8px;
            height: 8px;

            border-radius: 50%;
            background: #3fb950;

            box-shadow: 0 0 8px #3fb950;
        }

        .camera-card {
            overflow: hidden;

            background: #010409;

            border: 1px solid #30363d;
            border-radius: 14px;

            box-shadow:
                0 8px 30px rgba(0, 0, 0, 0.35);
        }

        .camera-header {
            display: flex;
            justify-content: space-between;
            align-items: center;

            padding: 12px 16px;

            background: #161b22;
            border-bottom: 1px solid #30363d;

            color: #8b949e;
            font-size: 13px;
        }

        .camera-title {
            color: #e6edf3;
            font-weight: 500;
        }

        .video-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;

            background: #000;

            padding: 20px;
        }

        .video-wrapper img {
            display: block;

            width: min(100%, 900px);
            height: auto;

            border-radius: 8px;

            box-shadow:
                0 0 0 1px rgba(255,255,255,0.05);
        }

        .info-grid {
            display: grid;

            grid-template-columns:
                repeat(auto-fit, minmax(160px, 1fr));

            gap: 12px;

            margin-top: 16px;
        }

        .info-card {
            padding: 16px;

            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 10px;
        }

        .info-label {
            color: #8b949e;
            font-size: 12px;

            margin-bottom: 6px;
        }

        .info-value {
            font-size: 16px;
            font-weight: 500;
        }

        footer {
            margin-top: 24px;

            color: #484f58;
            font-size: 12px;

            text-align: center;
        }

    </style>
</head>


<body>

<div class="container">

    <header>

        <div class="brand">

            <div class="logo">
                🦗
            </div>

            <div>
                <h1>MantisCV</h1>

                <div class="subtitle">
                    Autonomous Tennis Ball Tracker
                </div>
            </div>

        </div>


        <div class="status">

            <div class="status-dot"></div>

            CAMERA ONLINE

        </div>

    </header>


    <div class="camera-card">

        <div class="camera-header">

            <span class="camera-title">
                Live Camera
            </span>

            <span>
                MJPEG · 640×480 · 30 FPS
            </span>

        </div>


        <div class="video-wrapper">

            <img src="/stream" alt="Camera stream">

        </div>

    </div>


    <div class="info-grid">

        <div class="info-card">

            <div class="info-label">
                CAMERA
            </div>

            <div class="info-value">
                Logitech C270
            </div>

        </div>


        <div class="info-card">

            <div class="info-label">
                RESOLUTION
            </div>

            <div class="info-value">
                640 × 480
            </div>

        </div>


        <div class="info-card">

            <div class="info-label">
                FRAME RATE
            </div>

            <div class="info-value">
                30 FPS
            </div>

        </div>


        <div class="info-card">

            <div class="info-label">
                TRACKING
            </div>

            <div class="info-value">
                Standby
            </div>

        </div>

    </div>


    <footer>
        MantisCV · Raspberry Pi 5
    </footer>

</div>

</body>

</html>
"""


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        threaded=True
    )
