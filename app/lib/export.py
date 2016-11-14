import os
import zipfile 

class Exporter:
    """Exports Notes to Markdown Files"""
    
    def __init__(self, user):
        self.directory = "/tmp/{0}".format(user.id)
        self.notes = user.notes.all()
        self.create_export_dir()
        self.zip_file = "/tmp/{0}/braindump_export.zip".format(user.id)

    def create_export_dir(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def export(self):
        with zipfile.ZipFile("{0}/braindump_export.zip".format(self.directory), "w") as export_file:
            for note in self.notes:
                file_name = "{0}/{1}.md".format(self.directory, note.title)
                zip_file_name = "{0}.md".format(note.title)
                file = open(file_name, "w")
                file.write(self.add_front_matter(note.title, note.created_date,note.notebook.title))
                file.write(note.body)
                file.close()
                export_file.write(file_name, zip_file_name)

    @staticmethod
    def add_front_matter(title, date, notebook):
        #TODO clean this up 
        frontmatter = "---\ntitle: {0}\ndate: {1}\nnotebook: {2}\n---\n".format(title, date, notebook)
        return frontmatter

    