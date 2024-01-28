def mdn_asterisk(mdn_decrypted):
    if not mdn_decrypted:
        return None

    return mdn_decrypted[:3] + mdn_decrypted[3:5] + "**" + mdn_decrypted[7:9] + '**'
