def checksum(data) -> bytes:
    """
    Get checksum of object
    """    
    
    crc = 0
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ 0x07) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
    return crc.to_bytes(1, 'big')

def calc_db_sum(db) -> bytes:
    """
    Calculate checksum of database
    
    Args:
        db (dict): Database to calculate checksum for
        
    Returns:
        bytes: Checksum byte
    """
    
    import json
    db_dict = {k.decode(): v.decode() for k, v in db.items() if k != b"_sum"}
    db_json = json.dumps(db_dict, sort_keys=True)
    db_bytes = db_json.encode('utf-8')
    return checksum(db_bytes)

def verify_db(db) -> bool:
    """
    Verify database integrity by comparing stored checksum with calculated one
    
    Args:
        db (dict): Database to verify
        
    Returns:
        bool: True if checksum matches, False otherwise
    """
    
    if b"_sum" not in db:
        return False
    stored_crc = db[b"_sum"]
    calculated_crc = calc_db_sum(db)
    return stored_crc == calculated_crc