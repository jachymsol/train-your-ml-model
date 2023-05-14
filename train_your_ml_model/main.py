import train_alpha as train
import upload_beta as upload
import yaml

def main():
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    while True:
        cmd = input("Enter Command: ")
        if cmd in ("exit", "quit", "q"):
            return
        elif cmd in ("upload"):
            upload.upload(config)
        elif cmd in ("evaluate"):
            train.train_dataset(config)
        elif cmd in ("undo"):
            upload.remove_last_image(config)
        elif cmd in ("config"):
            print(config)
        else: 
            # Display help
            print("Available commands: upload, evaluate, quit")


if __name__ == '__main__':
    main()