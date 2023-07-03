cp src/example_config.yaml src/config.yaml

mkdir -p games
mkdir -p datasets/train/house
mkdir -p datasets/train/tree

if [ ! -d datasets/test ]; then
    unzip -q test_images.zip -d ./datasets/
fi

sed -i "s:root:$(pwd):g" src/config.yaml
