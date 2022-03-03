import uuid
def genrated_ref_code():
    code=str(uuid.uuid4()).replace('-','')[:15]
    return code