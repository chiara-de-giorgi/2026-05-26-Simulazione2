from database.DB_connect import DBConnect
from model.arco import Arco
from model.names import Names


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllRatings():
        # Prende tutti gli stati --> Crea l'oggetto Country
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct r.avg_rating 
                    from ratings r
                    order by avg_rating """

        cursor.execute(query)

        for row in cursor:
            result.append(row['avg_rating'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(rat1, rat2):
        # Prende tutti gli stati --> Crea l'oggetto Country
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
            select distinct n.*
            from ratings r, role_mapping rm, names n
            where n.id = rm.name_id and r.movie_id = rm.movie_id 
                    and  r.avg_rating >= %s and r.avg_rating <= %s and YEAR(n.date_of_birth)<=2026 """

        cursor.execute(query, (rat1, rat2))

        for row in cursor:
            result.append(Names(**row))

        cursor.close()
        conn.close()
        return result



    @staticmethod
    def getAllEdges(idMapN, rat1, rat2):
        # Prende tutti gli stati --> Crea l'oggetto Country
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
                    select rm1.name_id as n1, rm2.name_id as n2, sum( cast(replace(replace(m.worlwide_gross_income, '$', ''),',', '') as unsigned)) as peso
                    from movie m, role_mapping rm1, role_mapping rm2, ratings r, names n1, names n2
                    where m.id = rm1.movie_id
                    and m.id = rm2.movie_id
                    and m.id = r.movie_id
                    and rm1.name_id = n1.id
                    and rm2.name_id = n2.id
                    and n1.date_of_birth IS NOT NULL
                    and n2.date_of_birth IS NOT NULL
                    and rm1.name_id < rm2.name_id
                    and m.worlwide_gross_income is not null
                    and m.worlwide_gross_income like '$%'
                    and r.avg_rating >= %s
                    and r.avg_rating <= %s
                    group by rm1.name_id, rm2.name_id
                    """

        cursor.execute(query, (rat1, rat2))

        for row in cursor:
            n1=idMapN[row['n1']]
            n2=idMapN[row['n2']]
            peso=row['peso']
            result.append(Arco(n1, n2, peso))

        cursor.close()
        conn.close()
        return result