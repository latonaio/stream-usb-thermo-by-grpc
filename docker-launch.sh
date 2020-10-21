image_tag='stream-usb-thermo-by-grpc-server'
# GUI不要の場合、--deviceのみでOK
# GUI用にすべてのX接続を受け入れる
xhost +
docker run --privileged -it \
# -e DISPLAY=$DISPLAY \ # Xの宛先をホストと同一に
# -v /tmp/.X11-unix:/tmp/.X11-unix:rw \ # Xソケットを共有
--device /dev/video0:/dev/video0:mwr \ # カメラデバイスを共有
--device /dev/video1:/dev/video1:mwr \ # 複数指定も可能
${image_tag} /bin/bash