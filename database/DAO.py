from database.DB_connect import DBConnect
from model.gene import Gene


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllGenes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """
                    SELECT *
                    from genes g 
                """

        cursor.execute(query)

        for row in cursor:
            result.append(Gene(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllChromosomes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                    SELECT DISTINCT Chromosome 
                    FROM genes g
                    WHERE Chromosome > 0   
                """

        cursor.execute(query)

        for row in cursor:
            result.append(row["Chromosome"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllConnections():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                    SELECT g1.GeneID as Gene1, g2.GeneID as Gene2, i.Expression_Corr
                    from genes g1, genes g2, interactions i 
                    where g1.GeneId = i.GeneID1
                    and g2.GeneID = i.GeneID2 
                    and g1.Chromosome != g2.Chromosome 
                    and g1.Chromosome > 0
                    and g2.Chromosome > 0 
                    GROUP by g1.GeneID, g2.GeneID
                """

        cursor.execute(query)

        for row in cursor:
            result.append((row["Gene1"], row["Gene2"], row["Expression_Corr"]))

        cursor.close()
        conn.close()
        return result
