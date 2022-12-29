import os.path

from tkinter import Tk, Button, Label
from tkinter.ttk import Treeview
from tkinter.filedialog import askopenfilenames

from controllers import controller
from models.uploaded_image import ImageClazz

EXTENSIONS = [('Image Files', ('*jpg', '*png', '*webp', '*jpeg'))]


class ImageHandler(object):
    def __init__(self):
        self.root = Tk()
        self.root.title('Image Handler')
        self.root.geometry('510x400')
        self.root.resizable(width=False, height=False)

        self.images: list[ImageClazz] = []

        self.label_info = Label(self.root, text='Select files to resize')
        self.label_info.grid(row=0, column=0)

        self.upload_button = Button(self.root,
                                    text='Choose images',
                                    width=30,
                                    command=lambda: self.open_files())
        self.upload_button.grid(row=0, column=1)

        self.conversion_button = Button(self.root,
                                        text='Start conversion',
                                        width=30,
                                        command=lambda:
                                        self.completion_handler(self.images))
        self.conversion_button.grid(row=5, column=1, padx=10)

        self.folder_with_images = Button(self.root,
                                         text='Open folder',
                                         width=30,
                                         command=lambda:
                                         self.open_directory_with_files())

        self.folder_with_images.grid(row=5, column=0, padx=10)
        self.tree_view = Treeview(self.root, selectmode='browse', height=15)
        self.tree_view.grid(row=1, column=0, columnspan=2, padx=20, pady=5)
        self.tree_view['columns'] = ('Path', 'Status', 'File Size')
        self.tree_view['show'] = 'tree headings'
        self.tree_view.column('#0', width=20)
        self.tree_view.heading('#0', text='#')
        self.tree_view.column('Path', width=300)
        self.tree_view.heading('Path', text='Path')
        self.tree_view.column('Status', width=100)
        self.tree_view.heading('Status', text='Status')
        self.tree_view.column('File Size', width=50)
        self.tree_view.heading('File Size', text='File Size')
        self.root.mainloop()

    def open_files(self):
        image_paths = list(askopenfilenames(filetypes=EXTENSIONS))
        # After another upload files clear tree
        self.clear_tree()
        self.images: list[ImageClazz] = controller.create_image_entities(
            image_paths
        )
        for index, image in enumerate(self.images):
            self.tree_view.insert('', 'end', values=(image.get_image_path(),))
            self.change_status_column(index, 'Loaded')
            self.update_file_size_column(index,
                                         image_size=image.get_image_size())

    def clear_tree(self):
        if self.tree_view:
            for row in self.tree_view.get_children():
                self.tree_view.delete(row)

    def change_status_column(self, index, value):
        self.tree_view.set(item=self.tree_view.get_children()[index],
                           column='Status',
                           value=value)

    def update_file_size_column(self, index, image_size):
        self.tree_view.set(item=self.tree_view.get_children()[index],
                           column='File Size',
                           value=str(image_size) + 'KB')

    # TODO Add callback when image converted
    def completion_handler(self, images: list[ImageClazz]):
        controller.start_conversion(images)
        map(lambda x: images[x].update_image_size(), images)
        for index, image in enumerate(images):
            self.change_status_column(index, 'Changed')
            self.update_file_size_column(index, image.get_image_size())

    def open_directory_with_files(self):
        if self.tree_view.get_children():
            # .realpath() return path with switched slash to backslash
            path = os.path.realpath(
                os.path.dirname(self.images[0].get_image_path())
            )
            os.startfile(path)


if __name__ == '__main__':
    ImageHandler()
