from sklearn import svm
from sklearn.externals import joblib
import tornado.ioloop
import tornado.web
import sqlite3
import json
from calcoloArea import calcoloFeatures

class dataUpdate(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    def get(self):
        self.post()

    def post(self):
        nome=self.get_argument("nomeComponente",True)
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        """
        LOADING DATA
        """
        c.execute("SELECT * FROM Componente INNER JOIN Coordinate ON Componente.Nome=Coordinate.Nome_Componente WHERE Componente.Nome='"+nome+"'")
        data=c.fetchall()
        dataZone={}
        dataX={}
        dataY={}
        dataZ={}
        state={}
        for d in data:
            if (d[0] not in dataZone):
                dataX[d[0]]=[]
                dataY[d[0]]=[]
                dataZ[d[0]]=[]
            dataZone[d[0]]=d[1]
            dataX[d[0]].append(d[3])
            dataY[d[0]].append(d[4])
            dataZ[d[0]].append(d[5])
        features=[]
        featX1,featX2,featX3,featX4,featX5,featX6=calcoloFeatures(dataX[nome][len(dataX[nome])-100:])
        featY1,featY2,featY3,featY4,featY5,featY6=calcoloFeatures(dataY[nome][len(dataY[nome])-100:])
        featZ1,featZ2,featZ3,featZ4,featZ5,featZ6=calcoloFeatures(dataZ[nome][len(dataZ[nome])-100:])
        features.append([featX1,featX2,featX3,featX4,featX5,featX6,featY1,featY2,featY3,featY4,featY5,featY6,featZ1,featZ2,featZ3,featZ4,featZ5,featZ6])
        state[nome]=clf.predict(features)
        print(state)
        data={
            "nome":nome,
            "settore":dataZone[nome],
            "datiX":dataX[nome][len(dataX[nome])-200:],
            "datiY":dataY[nome][len(dataY[nome])-200:],
            "datiZ":dataZ[nome][len(dataZ[nome])-200:],
            "statoAttuale":label[state[nome][0]]
            }
        #print(data)
        self.write(json.dumps(data))
        conn.close()
class loadRefData(tornado.web.RequestHandler):
	def set_default_headers(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

	def options(self):
		# no body
		self.set_status(204)
		self.finish()

	def get(self):
		self.post()

	def post(self):
		conn = sqlite3.connect('data.db')
		c = conn.cursor()
		"""
        LOADING DATA
        """
		c.execute("SELECT * FROM Componente INNER JOIN Coordinate ON Coordinate.Nome_Componente='Ventola-Buona'")
		data=c.fetchall()
		dataZone={}
		dataX={}
		dataY={}
		dataZ={}
		state={}
		
		for d in data:
			if (d[0] not in dataZone):
				dataX[d[0]]=[]
				dataY[d[0]]=[]
				dataZ[d[0]]=[]
			dataZone[d[0]]=d[1]
			dataX[d[0]].append(d[3])
			dataY[d[0]].append(d[4])
			dataZ[d[0]].append(d[5])


		data=[]
		for k in dataZone.keys():
			features=[]
			featX1,featX2,featX3,featX4,featX5,featX6=calcoloFeatures(dataX[k][100:200])
			featY1,featY2,featY3,featY4,featY5,featY6=calcoloFeatures(dataY[k][100:200])
			featZ1,featZ2,featZ3,featZ4,featZ5,featZ6=calcoloFeatures(dataZ[k][100:200])
			features.append([featX1,featX2,featX3,featX4,featX5,featX6,featY1,featY2,featY3,featY4,featY5,featY6,featZ1,featZ2,featZ3,featZ4,featZ5,featZ6])
			state[k]=clf.predict(features)

            #print(state[k][0])
			data.append({
				"nome":k,
				"settore":dataZone[k],
				"datiX":dataX[k][:200],
				"datiY":dataY[k][:200],
				"datiZ":dataZ[k][:200],
				"statoAttuale":label[state[k][0]]
			})
        #print(data)
		self.write(json.dumps(data))
		conn.close()
	
class loadData(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    def get(self):
        self.post()

    def post(self):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        """
        LOADING DATA
        """
        c.execute("SELECT * FROM Componente INNER JOIN Coordinate ON Componente.Nome=Coordinate.Nome_Componente")
        data=c.fetchall()
        dataZone={}
        dataX={}
        dataY={}
        dataZ={}
        state={}

        for d in data:
            if (d[0] not in dataZone):
                dataX[d[0]]=[]
                dataY[d[0]]=[]
                dataZ[d[0]]=[]
            dataZone[d[0]]=d[1]
            dataX[d[0]].append(d[3])
            dataY[d[0]].append(d[4])
            dataZ[d[0]].append(d[5])


        data=[]
        for k in dataZone.keys():
            features=[]
            featX1,featX2,featX3,featX4,featX5,featX6=calcoloFeatures(dataX[k][len(dataX[k])-100:])
            featY1,featY2,featY3,featY4,featY5,featY6=calcoloFeatures(dataY[k][len(dataY[k])-100:])
            featZ1,featZ2,featZ3,featZ4,featZ5,featZ6=calcoloFeatures(dataZ[k][len(dataZ[k])-100:])
            features.append([featX1,featX2,featX3,featX4,featX5,featX6,featY1,featY2,featY3,featY4,featY5,featY6,featZ1,featZ2,featZ3,featZ4,featZ5,featZ6])
            state[k]=clf.predict(features)

            #print(state[k][0])
            data.append({
                "nome":k,
                "settore":dataZone[k],
                "datiX":dataX[k][len(dataX[k])-200:],
                "datiY":dataY[k][len(dataY[k])-200:],
                "datiZ":dataZ[k][len(dataZ[k])-200:],
                "statoAttuale":label[state[k][0]]
            })
        #print(data)
        self.write(json.dumps(data))
        conn.close()


if __name__ == "__main__":
	label=["rotto","danneggiato","buono"]
	clf = joblib.load('net4.pkl')
	application = tornado.web.Application([
        (r"/loadData", loadData),
        (r"/dataUpdate", dataUpdate),
        (r"/loadRefData", loadRefData)
	])
	application.listen(9000)
	print("Starting server...")
	tornado.ioloop.IOLoop.current().start()
