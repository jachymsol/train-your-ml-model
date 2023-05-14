import train_alpha as train
import upload_alpha as upload
import config

def main():
    while True:
        cmd = input("Enter Command: ")
        if cmd in ("exit", "quit", "q"):
            return
        elif cmd in ("upload"):
            upload.upload()
        elif cmd in ("evaluate"):
            train.train_dataset()
        elif cmd in ("undo"):
            upload.remove_last_image()
        elif cmd in ("config"):
            config.print_config()
        else: 
            # Display help
            print("Available commands: upload, evaluate, quit")


if __name__ == '__main__':
    main()