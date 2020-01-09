import imageio
import os
import imageio_ffmpeg

def write_video_to_stream(path_to_video, rtp_port):
    video_reader = imageio.get_reader(path_to_video)
    img_writer = None
    rtp_url = f"rtp://localhost:{rtp_port}"
    output_params = [ '-f', 'rtp_mpegts']
    input_params = ['-re']
    for frame in video_reader:
        if img_writer is None:
            img_writer = imageio_ffmpeg.write_frames(
                    rtp_url,
                    size=(frame.shape[1], frame.shape[0]),
                    output_params=output_params,
                    input_params=input_params,
                    fps=24,
                    codec='mpeg4',
                    bitrate='1024K'
                    )
            img_writer.send(None)
        try:
            img_writer.send(frame)
        except KeyboardInterrupt as e:
            img_writer.close()
            break
    img_writer.close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_video")
    parser.add_argument("rtp_port")
    ns = parser.parse_args()
    write_video_to_stream(ns.path_to_video, ns.rtp_port)
