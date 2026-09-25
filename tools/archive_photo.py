"""Archive a JPEG without private metadata; preserve compressed image pixels.
Usage: .venv/bin/python tools/archive_photo.py INPUT OUTPUT
Original stays untouched. Refuses rotated EXIF images or existing targets.
"""
import hashlib
import io
import json
from pathlib import Path
import sys
from PIL import Image

source,target=map(Path,sys.argv[1:])
assert not target.exists() and not target.with_suffix('.json').exists()
data=source.read_bytes()
assert data[:2]==b'\xff\xd8'
before=Image.open(io.BytesIO(data));before.load()
assert before.getexif().get(274,1)==1,'Orientation needs separate review'
out=bytearray(data[:2]);i=2;removed=[]
while i<len(data):
    start=i
    assert data[i]==255
    while data[i]==255:i+=1
    marker=data[i];i+=1
    if marker==0xDA:  # Preserve complete entropy-coded image after start of scan.
        out.extend(data[start:]);break
    assert marker not in (0xD8,0xD9) and not 0xD0<=marker<=0xD7
    length=int.from_bytes(data[i:i+2],'big');end=i+length
    assert length>=2 and end<=len(data)
    # Keep only format/color interpretation markers, discard metadata/comments.
    if (0xE0<=marker<=0xEF and marker not in (0xE0,0xE2,0xEE)) or marker==0xFE:
        removed.append(hex(marker))
    else:out.extend(data[start:end])
    i=end
after=Image.open(io.BytesIO(out));after.load()
assert before.mode==after.mode and before.size==after.size and before.tobytes()==after.tobytes()
assert not after.getexif()
target.parent.mkdir(parents=True,exist_ok=True)
target.write_bytes(out)
record=dict(original_filename=source.name,original_sha256=hashlib.sha256(data).hexdigest(),public_filename=target.name,public_sha256=hashlib.sha256(out).hexdigest(),removed_marker_types=removed,decoded_pixels_identical=True,size=list(after.size),note='Metadata-stripped public copy; original upload unchanged and not committed.')
target.with_suffix('.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
