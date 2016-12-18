import os

from app import db
from app.models import Note, Notebook
from app.lib.export import Exporter

from api_base import ApiBaseTestCase


class NoteExportTestCase(ApiBaseTestCase):

    def test_special_character(self):

        u = self.add_user()

        nb = Notebook(title="default", author=u)
        db.session.add(nb)
        db.session.commit()

        n = Note(title="5/14/3", body="test", notebook_id=nb.id, author=u)
        db.session.add(n)
        db.session.commit()

        e = Exporter(u)
        e.export()

        note_files = os.listdir("/tmp/braindump-export/{0}".format(u.id))
        expected_note_file = "5-14-3.md"

        self.assertTrue(expected_note_file in note_files)

    def test_export_dir_created_when_not_exist(self):

        u = self.add_user()

        nb = Notebook(title="default", author=u)
        db.session.add(nb)
        db.session.commit()

        n = Note(title="5/14/3", body="test", notebook_id=nb.id, author=u)
        db.session.add(n)
        db.session.commit()

        # Create Two Exporter Instances
        e = Exporter(u)
        e2 = Exporter(u)

        e.export()
        e2.export()

        notebook_dir = os.listdir("/tmp/braindump-export")

        self.assertEqual(1, len(notebook_dir))



