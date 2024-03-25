"""Migrate a project from the old format to the new format."""

import datetime
import functools
import shutil
import sqlite3
from collections import namedtuple
from pathlib import Path
from typing import Callable
from urllib.parse import urlparse

from archeion.index.models import Artifact, Link


def namedtuple_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    cls = namedtuple("Row", fields)
    return cls._make(row)


def load_old_snapshots(db_path: Path):
    """Load the old data from the database."""
    con = sqlite3.connect(db_path)
    con.row_factory = namedtuple_factory
    cur = con.cursor()
    cur.execute("SELECT * FROM core_snapshot")
    return cur.fetchall()


def load_old_archiveresults(db_path: Path, snapshot_id: str) -> list:
    """Load the old data from the database."""
    con = sqlite3.connect(db_path)
    con.row_factory = namedtuple_factory
    cur = con.cursor()
    query = """
    SELECT *
    FROM core_archiveresult
    WHERE snapshot_id = ? AND extractor IN ('headers', 'pdf', 'screenshot', 'dom')
    ORDER BY start_ts
    """
    cur.execute(query, (snapshot_id,))
    return cur.fetchall()


def convert_snapshots(old_snapshots: list, get_archive_results: Callable, src_path: Path, dst_path: Path):
    """Convert the old snapshots to the new format."""
    from archeion.utils import normalize_url

    extractor_map = {
        "dom": "DOM",
        "pdf": "PDF",
        "screenshot": "screenshot",
        "headers": "headers",
    }
    output_map = {
        "output.html": "dom.html",
        "screenshot.png": "screenshot.png",
        "output.pdf": "print.pdf",
        "headers.json": "headers.json",
    }

    for snapshot in old_snapshots:
        print(f"Converting snapshot {snapshot.url}")
        normalized_url = normalize_url(snapshot.url)
        link = Link.objects.create(
            url=normalized_url,
            parsed_url=urlparse(normalized_url),
            title=snapshot.title,
            content_type="text/html",
            created_at=datetime.datetime.fromisoformat(snapshot.added).replace(tzinfo=datetime.timezone.utc),
            updated_at=datetime.datetime.fromisoformat(snapshot.updated).replace(tzinfo=datetime.timezone.utc),
        )
        link_path = dst_path.joinpath(f"{link.id}")
        link_path.mkdir(exist_ok=True)

        for archiveresult in get_archive_results(snapshot.id):
            print(f"  - Converting archive result {archiveresult.extractor}")
            if archiveresult.output not in output_map:
                print(f"    - Can't map: {archiveresult.output}")
                continue
            Artifact.objects.update_or_create(
                link=link,
                plugin_name=extractor_map[archiveresult.extractor],
                defaults={
                    "output_path": output_map[archiveresult.output],
                    "status": archiveresult.status,
                    "start_ts": datetime.datetime.fromisoformat(archiveresult.start_ts).replace(
                        tzinfo=datetime.timezone.utc
                    ),
                    "end_ts": datetime.datetime.fromisoformat(archiveresult.end_ts).replace(
                        tzinfo=datetime.timezone.utc
                    ),
                },
            )
            from_path = src_path.joinpath(f"{snapshot.timestamp}/{archiveresult.output}")
            to_path = link_path / output_map[archiveresult.output]
            if not from_path.exists():
                print(f"    - File {from_path} is missing.")
                continue
            if to_path.exists():
                print(f"    - File {to_path} exists. Skipping.")
            print(f"    - Copying {from_path} to {to_path}")
            shutil.copy(from_path, to_path)


def main():
    db_path = Path("/Users/OORDCOR/boxarchive/index.sqlite3")
    archivebox_path = Path("/Users/OORDCOR/boxarchive/archive")
    dest_path = Path("/Users/OORDCOR/Documents/code/archeion/archives/artifacts")
    get_archive_results = functools.partial(load_old_archiveresults, db_path)
    old_snapshots = load_old_snapshots(db_path)
    convert_snapshots(old_snapshots, get_archive_results, archivebox_path, dest_path)
