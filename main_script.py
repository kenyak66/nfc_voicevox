from NFCReader import NFCReader

class MainApplication:
    def __init__(self):
        self.nfc_reader = NFCReader()

    def run(self):
        while True:
            try:
                # NFCリーダーの実行
                self.nfc_reader.run()
            except KeyboardInterrupt:
                print("Exiting the application")
                break

if __name__ == "__main__":
    app = MainApplication()
    app.run()
