#!/usr/bin/python3

########################################################################
# Copyright (c) 2023 Contributors to the Eclipse Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
########################################################################

from dbcfeederlib import dbcparser, dbc2vssmapper
import os
from pathlib import Path
from cantools import logreader

# read config only once
my_path = Path(os.path.dirname(os.path.abspath(__file__)))
db_filename = str(my_path / "system-4.2.arxml")
can_trace_filename = str(my_path / "container_frame.log")
mapping_filename = str(my_path / "mapping_container_test.json")

def test_container_frames():
    mapper: dbc2vssmapper.Mapper = dbc2vssmapper.Mapper(
        mapping_definitions_file=mapping_filename,
        dbc_file_names=[db_filename])
    reader = logreader.Parser(open(can_trace_filename))
    for line, data in reader.iterlines(keep_unknowns=True):
        print(f"{line=}, {data.frame_id=}, {data.data.hex()=}")

if __name__ == "__main__":
    test_container_frames()
