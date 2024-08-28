#!/usr/bin/env python

#  COPYRIGHT Ericsson 2019
#  The copyright to the computer program(s) herein is the property of
#  Ericsson Inc. The programs may be used and/or copied only with written
#  permission from Ericsson Inc. or in accordance with the terms and
#  conditions stipulated in the agreement/contract under which the
#  program(s) have been supplied.

import argparse
import glob
import shutil
import xmltodict
import xmlplain
import zipfile
import os
from functools import partial
from json import loads, dumps


def unzip(input_file, output_path):
    """Unzips the input file.
    :param input_file: The input file.
    :param output_path: The output path directory.
    """
    with zipfile.ZipFile(input_file, 'r') as zref:
        zref.extractall(output_path)


def to_dict(xmlfile):
    """Loads a XML file into a dictionary.
    :param xmlfile: A string with the path of the XML file.
    :return: A dictionary with the contents of the file.
    """
    with open(xmlfile, "r", encoding='utf-8') as fd:
        return loads(dumps(xmltodict.parse(fd.read())))


def is_embedded_scripts(element):
    """Informs if the given dictionary property is an embedded script.
    :param element: A dictionary property, that should contain other dictionary.
    :rtype: bool
    """
    return element['@Name'] == 'EmbeddedScripts.xml'


def embres_path(embres_dict):
    """Finds the path of the embedded resources file.
    This file contains all the dxp scrips like IronPython and JavaScript.
    :param embres_dict: The dictionary with the 'EmbeddedResources.xml' file contents.
    :return: The path of the embedded resources file.
    :rtype: str
    """
    embedded_resources = embres_dict['EmbeddedResources']['EmbeddedResource']
    return list(filter(is_embedded_scripts, embedded_resources))[0]['@ArchiveElementPath']


def save_file(filepath, contents):
    """Saves a string to a file.
    :param filepath: The output file path.
    :param contents: The string to be saved.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding='utf-8') as f:
        f.write(contents)


def fix_chars(text):
    """Decode HTML chars in the string.
    :param text: The string to decode.
    :return: The decoded text.
    """
    try:
        text = text.replace('_x09', '\t')
        text = text.replace('&amp;', '&')
        text = text.replace('&gt;', '>')
        text = text.replace('&lt;', '<')
        text = text.replace('&quot;', '"')
        return text
    except AttributeError:
        return ''


def file_ext(etype):
    """Return the file extension for the given element type.
    :param etype: A string with the element type.
    :return: A string with the file extension.
    :rtype: str
    """
    if etype == 'JavaScript':
        return '.js'
    elif etype == 'IronPython':
        return '.py'
    else:
        # Don't put an extension.
        return ''


def unpack_dxp(input_dxp, output_path, output_src='src'):
    """Unpack a dxp file to a specified path.
    :param input_dxp: A string with the path of the dxp file.
    :param output_path: A string with the output path for the contents of the dxp.
    :param output_src: A string with the output path for the code assets, like IronPython and JavaScript files.
    """
    # The file path of the XML file that contains the indexes of the source code
    embres_metafile = f'{output_path}/EmbeddedResources.xml'

    unzip(input_dxp, output_path)

    emb_res = to_dict(embres_metafile)
    embres_file = output_path + '/' + embres_path(emb_res)
    embscripts = to_dict(embres_file)['EmbeddedScripts']

    if embscripts:
        scripts = embscripts['EmbeddedScript']
        for s in scripts:
            sid = s['@ManagedScriptId']
            sdef = s['ScriptDefinition']
            sname = sdef['@Name']
            lang = sdef['@LanguageName']
            scode = sdef['ScriptCode']
            fext = file_ext(lang)
            filepath = f'{output_src}/{lang}/{sname}{fext}'
            save_file(filepath, fix_chars(scode))


def get_dxp_files():
    """Return all dxp files in the actual directory.
    :return A list with the location of each dxp file found, if any.
    :rtype: list
    """
    return [f for f in glob.glob('*.dxp')]


def print_it(text, silent=False):
    """Print the text to the standard output.
    :param text: The text to be printed.
    :param silent: A boolean indicating if the print should be ignored.
    """
    if not silent:
        print(text)


def process_command_line():
    """The entry point of this module, processes the command line via standard UNIX command line arguments."""

    dxp_files = get_dxp_files()
    i_flag_required = len(dxp_files) != 1

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input-file',
                        required=i_flag_required,
                        type=str,
                        default=None,
                        metavar="<input-dxp-file>",
                        help="The dxp file to extract the source code, if more than one file is present in the actual"
                             "directory. If only one file is present, the tool will pick up the file automatically.")

    parser.add_argument('-oc', '--output-contents',
                        required=False,
                        type=str,
                        default='dxp_contents',
                        metavar="<dxp-output-path>",
                        help="The output path for extracting the contents of dxp")

    parser.add_argument('-os', '--output-sources',
                        required=False,
                        type=str,
                        default='src',
                        metavar="<src-output-path>",
                        help="The output path for putting the source code extracted from the input file")

    parser.add_argument('-pc', '--preserve-contents',
                        required=False,
                        action='store_true',  # No arguments
                        help="Preserves the output contents directory after extracting the files")

    parser.add_argument('-s', '--silent',
                        required=False,
                        action='store_true',  # No arguments
                        help="Silent option, don't print any messages")

    args = parser.parse_args()

    log = partial(print_it, silent=args.silent)

    dxp_file = args.input_file or dxp_files[0]
    log(f'Unpacking files from \'{dxp_file}\'...')

    unpack_dxp(dxp_file, args.output_contents, args.output_sources)

    if not args.preserve_contents:
        shutil.rmtree(args.output_contents, ignore_errors=True)

    log('Done.')


if __name__ == "__main__":
    process_command_line()
