import json
import threading
import unittest
import urllib.error
import urllib.request

import app


class NotesApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.NOTES.clear()
        cls.server = app.make_server(0)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def url(self, path):
        return f"http://127.0.0.1:{self.port}{path}"

    def test_healthz_returns_ok(self):
        with urllib.request.urlopen(self.url("/healthz")) as r:
            self.assertEqual(r.status, 200)
            self.assertEqual(json.loads(r.read())["status"], "ok")

    def test_add_and_list_note(self):
        req = urllib.request.Request(
            self.url("/notes"),
            data=json.dumps({"text": "hello"}).encode(),
            method="POST",
        )
        with urllib.request.urlopen(req) as r:
            self.assertEqual(r.status, 201)
        with urllib.request.urlopen(self.url("/notes")) as r:
            notes = json.loads(r.read())
        self.assertIn("hello", [n["text"] for n in notes])

    def test_empty_note_is_rejected(self):
        req = urllib.request.Request(self.url("/notes"), data=b"{}", method="POST")
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req)
        self.assertEqual(ctx.exception.code, 400)


if __name__ == "__main__":
    unittest.main()
