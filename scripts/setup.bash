mkdir -p games
mkdir -p datasets/train/house
mkdir -p datasets/train/tree

unzip -q test_images.zip -d ./datasets/

sed -i "s:root:$(pwd):g" src/config.yaml
