import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._rate1Value = None
        self._rate2Value= None

    def fillDDsRating(self):
        ratings =self._model.getAllRatings()
        shapeDD1Option = list(map(lambda x: ft.dropdown.Option(data=x, key=x, on_click=self._choiceDDRate1), ratings))
        shapeDD2Option = list(map(lambda x: ft.dropdown.Option(data=x, key=x, on_click=self._choiceDDRate2), ratings))
        self._view._ddrating1.options = shapeDD1Option
        self._view._ddrating2.options=shapeDD2Option
        self._view.update_page()

    def _choiceDDRate1(self, e):
        self._rate1Value = e.control.data

    def _choiceDDRate2(self, e):
        self._rate2Value = e.control.data

    def handleCreaGrafo(self, e):
        rate1=float(self._rate1Value)
        rate2=float(self._rate2Value)

        if rate1 is None or rate2 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzionare, selezionare un range di valutazioni per procedere!", color="red"))
            self._view.update_page()

        if rate1 >= rate2:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzionare, selezionare un range di valutazioni valido per procedere!", color="red"))
            self._view.update_page()

        self._model.buildGraph(rate1, rate2)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato!"))
        n, a = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {n}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {a}"))

        top5archi=self._model.get5BestEdges()
        self._view.txt_result.controls.append(ft.Text("Top 5 archi:"))
        for u, v, peso in top5archi:
            self._view.txt_result.controls.append(ft.Text(f"{u} -> {v}: {peso} "))

        compConn=self._model.getConnectedComponents()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {len(compConn)} componenti connesse"))
        maxCompConn=self._model.maxCompConnesse()
        self._view.txt_result.controls.append(ft.Text(f"La più grande componente connessa è lunga {len(maxCompConn)}"))
        for n in maxCompConn:
            self._view.txt_result.controls.append(ft.Text(n))

        self._view.update_page()

    def handleCammino(self, e):
        path= self._model.getBestPath()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Ho trovato un cammino ottimo di lunghezza {len(path)}"))
        for n in path:
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.update_page()

