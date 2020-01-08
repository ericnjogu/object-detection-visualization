import imageio
import asyncio
import os
import imageio_ffmpeg

async def write_video_to_stream(path_to_video, path_to_socket):
    video_reader = imageio.get_reader(path_to_video)
    sock = await create_socket(path_to_socket)
    _, socket_writer = await asyncio.open_unix_connection(sock=sock)
    img_writer = None
    for frame in video_reader:
        if img_writer is None:
            img_writer = imageio_ffmpeg.write_frames(socket_writer, size=(frame.shape[1], frame.shape[0]))
            img_writer.send(None)
        img_writer.send(frame)
        await socket_writer.drain()
    img_writer.close()
    socket_writer.close()

async def create_socket(path_to_socket):
    # credit - https://serverfault.com/a/914572/57785
    import socket
    sock = socket.socket(socket.AF_UNIX)
    # credit - https://pymotw.com/2/socket/uds.html
    if os.path.exists(path_to_socket):
        os.unlink(path_to_socket)
    sock.bind(path_to_socket)
    return sock


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_video")
    parser.add_argument("path_to_socket")
    ns = parser.parse_args()
    asyncio.run(write_video_to_stream(ns.path_to_video, ns.path_to_socket))
