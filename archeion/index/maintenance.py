"""Functions to maintain the archive and index."""
from typing import List, Tuple

from django.core.files.storage import Storage


def fix_invalid_folder_locations(storage: Storage) -> Tuple[List[str], List[str]]:
    return ([], [])
    # fixed = []
    # cant_fix = []
    # for dirs, _ in storage.listdir("."):
    #     for dir in dirs:
    #         if (Path(entry.path) / 'index.json').exists():
    #             try:
    #                 link = parse_json_link_details(entry.path)
    #             except KeyError:
    #                 link = None
    #             if not link:
    #                 continue
    #
    #             if not entry.path.endswith(f'/{link.timestamp}'):
    #                 dest = out_dir / ARCHIVE_DIR_NAME / link.timestamp
    #                 if dest.exists():
    #                     cant_fix.append(entry.path)
    #                 else:
    #                     shutil.move(entry.path, dest)
    #                     fixed.append(dest)
    #                     timestamp = entry.path.rsplit('/', 1)[-1]
    #                     assert link.link_dir == entry.path
    #                     assert link.timestamp == timestamp
    #                     write_json_link_details(link, out_dir=entry.path)
    #
    # return fixed, cant_fix


def check_artifacts(storage: Storage) -> None:
    """Check that the artifacts archived match the index."""
    pass
    # from archeion.index.models import Link
    #
    # CONSOLE.print('[green]:white_check_mark: Checking links from indexes and artifact folders (safe to Ctrl+C)...[/]')
    #
    # all_links = Link.objects.all()
    #
    # CONSOLE.print(Padding(f":white_check_mark: Loaded {all_links.count()} links from existing main index.", (1, 0, 0, 2)))
    #
    # try:
    #     # Links in data folders that don't match their timestamp
    #     fixed, cant_fix = fix_invalid_folder_locations(storage)
    #     if fixed:
    #         print(
    #             '    {lightyellow}√ Fixed {} data directory locations that didn\'t match their link timestamps.{reset}'.format(
    #                 len(fixed), **ANSI))
    #     if cant_fix:
    #         print(
    #             '    {lightyellow}! Could not fix {} data directory locations due to conflicts with existing folders.{reset}'.format(
    #                 len(cant_fix), **ANSI))
    #
    #     # Links in JSON index but not in main index
    #     orphaned_json_links = {
    #         link.url: link
    #         for link in parse_json_main_index(out_dir)
    #         if not all_links.filter(url=link.url).exists()
    #     }
    #     if orphaned_json_links:
    #         pending_links.update(orphaned_json_links)
    #         print('    {lightyellow}√ Added {} orphaned links from existing JSON index...{reset}'.format(
    #             len(orphaned_json_links), **ANSI))
    #
    #     # Links in data dir indexes but not in main index
    #     orphaned_data_dir_links = {
    #         link.url: link
    #         for link in parse_json_links_details(out_dir)
    #         if not all_links.filter(url=link.url).exists()
    #     }
    #     if orphaned_data_dir_links:
    #         pending_links.update(orphaned_data_dir_links)
    #         print('    {lightyellow}√ Added {} orphaned links from existing archive directories.{reset}'.format(
    #             len(orphaned_data_dir_links), **ANSI))
    #
    #     # Links in invalid/duplicate data dirs
    #     invalid_folders = {
    #         folder: link
    #         for folder, link in get_invalid_folders(all_links, out_dir=out_dir).items()
    #     }
    #     if invalid_folders:
    #         print('    {lightyellow}! Skipped adding {} invalid link data directories.{reset}'.format(
    #             len(invalid_folders), **ANSI))
    #         print('        X ' + '\n        X '.join(
    #             f'./{Path(folder).relative_to(OUTPUT_DIR)} {link}' for folder, link in invalid_folders.items()))
    #         print()
    #         print(
    #             '    {lightred}Hint:{reset} For more information about the link data directories that were skipped, run:'.format(
    #                 **ANSI))
    #         print('        archivebox status')
    #         print('        archivebox list --status=invalid')
    #
    # except (KeyboardInterrupt, SystemExit) as e:
    #     ERR_CONSOLE.print("[red]:x: Stopped checking artifact directories due to Ctrl-C/SIGTERM[/]")
    #     raise Abort() from e
    #
    # write_main_index(list(pending_links.values()), out_dir=out_dir)
    #
    # print('\n{green}----------------------------------------------------------------------{reset}'.format(**ANSI))
    # if existing_index:
    #     print('{green}[√] Done. Verified and updated the existing ArchiveBox collection.{reset}'.format(**ANSI))
    # else:
    #     # TODO: allow creating new supersuer via env vars on first init
    #     # if config.HTTP_USER and config.HTTP_PASS:
    #     #     from django.contrib.auth.models import User
    #     #     User.objects.create_superuser(HTTP_USER, '', HTTP_PASS)
    #
    #     print('{green}[√] Done. A new ArchiveBox collection was initialized ({} links).{reset}'.format(
    #         len(all_links) + len(pending_links), **ANSI))
    #
    # json_index = out_dir / JSON_INDEX_FILENAME
    # html_index = out_dir / HTML_INDEX_FILENAME
    # index_name = f"{date.today()}_index_old"
    # if json_index.exists():
    #     json_index.rename(f"{index_name}.json")
    # if html_index.exists():
    #     html_index.rename(f"{index_name}.html")
    #
    # if setup:
    #     run_subcommand('setup', pwd=out_dir)
    #
    # if Snapshot.objects.count() < 25:  # hide the hints for experienced users
    #     print()
    #     print('    {lightred}Hint:{reset} To view your archive index, run:'.format(**ANSI))
    #     print('        archivebox server  # then visit http://127.0.0.1:8000')
    #     print()
    #     print('    To add new links, you can run:')
    #     print("        archivebox add < ~/some/path/to/list_of_links.txt")
    #     print()
    #     print('    For more usage and examples, run:')
    #     print('        archivebox help')
