import sqlite3

db = 'properties.db'

def update_notified_status(properties):
    # filter properties with notified=1
    notified_properties = [prop for prop in properties if prop.get('notified', 0) == 1]
    notified_ids = [prop['id'] for prop in notified_properties]
    if notified_ids:
        stmt = "UPDATE properties SET notified = 1 WHERE id IN ({})".format(','.join(['?'] * len(notified_ids)))
        
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        
        # Update the notified column to 1
        cursor.execute(stmt, notified_ids)
        
        conn.commit()

        rows_affected = cursor.rowcount
        print(f"Filas actualizadas: {rows_affected}")
        conn.close()