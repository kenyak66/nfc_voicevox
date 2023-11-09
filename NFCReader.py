import nfc
from voicevox import text_to_speech

class NFCReader:
    def __init__(self):
        pass

    def sc_from_raw(self, sc):
        return nfc.tag.tt3.ServiceCode(sc >> 6, sc & 0x3f)

    def on_startup(self, targets):
        print("waiting for new NFC tags...")
        return targets

    def get_id(self, tag):
        sc1 = self.sc_from_raw(0x200B)
        bc1 = nfc.tag.tt3.BlockCode(0, service=0)
        bc2 = nfc.tag.tt3.BlockCode(1, service=0)
        block_data = tag.read_without_encryption([sc1], [bc1, bc2])
        student_id = block_data[1:9].decode("utf-8")
        print("学生番号: " + student_id)
        return student_id

    def on_connect(self, tag):
        print("[*] connected:", tag)
        student_id = self.get_id(tag)
        # 音声合成
        text_to_speech(f"学籍番号 {student_id}。お疲れ様です！今日も一日頑張りましたね！")
        return True

    def on_release(self, tag):
        print("[*] released:", tag)

    def run(self):
        clf = nfc.ContactlessFrontend('usb')
        if clf:
            while clf.connect(rdwr={
                'on-startup': self.on_startup,
                'on-connect': self.on_connect,
                'on-get_id': self.get_id,
                'on-release': self.on_release,
            }):
                pass
