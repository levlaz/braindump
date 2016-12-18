import os
import zipfile
from slugify import slugify


class Exporter(object):
    """Exports Notes to Markdown Files"""

    def __init__(self, user):
        self.directory = "/tmp/braindump-export/{0}".format(user.id)
        self.notes = user.notes.all()
        self.create_export_dir()
        self.zip_file = "/tmp/braindump-export/{0}/braindump_export.zip".format(user.id)

    def create_export_dir(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def export(self):
        with zipfile.ZipFile("{0}/braindump_export.zip".format(self.directory), "w") as export_file:
            for note in self.notes:
                file_name = "{0}/{1}.md".format(self.directory, slugify(note.title))
                zip_file_name = "{0}.md".format(slugify(note.title))
                note_file = open(file_name, "w")
                note_file.write(self.add_front_matter(
                    note.title, note.created_date, note.notebook.title))
                note_file.write(note.body)
                note_file.close()
                export_file.write(file_name, zip_file_name)

    @staticmethod
    def add_front_matter(title, date, notebook):
        """Add metadata to each note"""
        # FIXME clean this up
        frontmatter = "---\ntitle: {0}\ndate: {1}\nnotebook: {2}\n---\n".format(
            title, date, notebook)
        return frontmatter

