import pathlib as pl
import shutil
import uuid


class NoNestedFolder(Exception):
    pass


class NoIndexHtml(Exception):
    pass


def make_a_zip_file(dirpath: pl.Path) -> pl.Path:

    zipfile_filename = str(uuid.uuid4())
    shutil.make_archive(zipfile_filename, "zip", dirpath)
    return pl.Path(zipfile_filename + ".zip")


def make_sure_theres_a_nested_folder_and_index_html(dirpath: pl.Path) -> None:
    if "folder" not in [d.name for d in list(dirpath.iterdir())]:
        raise NoNestedFolder(
            "Please create a folder in the root of the site's directory, and put all the files in there."
        )

    if "index.html" not in [i.name for i in list((dirpath / "folder").iterdir())]:
        raise NoIndexHtml
