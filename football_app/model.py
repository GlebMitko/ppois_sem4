import xml.dom.minidom
import xml.sax
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class FootballPlayer:
    full_name: str  # ФИО игрока
    birth_date: datetime  # Дата рождения
    team: str  # Футбольная команда
    home_city: str  # Домашний город
    lineup: str  # Состав (основной/запасной)
    position: str  # Позиция

    def to_xml_element(self, doc: xml.dom.minidom.Document):
        el = doc.createElement("player")

        full_name_el = doc.createElement("full_name")
        full_name_el.appendChild(doc.createTextNode(self.full_name))
        el.appendChild(full_name_el)

        birth_date_el = doc.createElement("birth_date")
        birth_date_el.appendChild(doc.createTextNode(self.birth_date.strftime("%Y-%m-%d")))
        el.appendChild(birth_date_el)

        team_el = doc.createElement("team")
        team_el.appendChild(doc.createTextNode(self.team))
        el.appendChild(team_el)

        home_city_el = doc.createElement("home_city")
        home_city_el.appendChild(doc.createTextNode(self.home_city))
        el.appendChild(home_city_el)

        lineup_el = doc.createElement("lineup")
        lineup_el.appendChild(doc.createTextNode(self.lineup))
        el.appendChild(lineup_el)

        position_el = doc.createElement("position")
        position_el.appendChild(doc.createTextNode(self.position))
        el.appendChild(position_el)

        return el


# SAX парсер для загрузки
class PlayerHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.players = []
        self.current_tag = ""
        self.current_player = {}

    def startElement(self, name, attrs):
        self.current_tag = name
        if name == "player":
            self.current_player = {}

    def endElement(self, name):
        if name == "player":
            self.players.append(FootballPlayer(
                full_name=self.current_player.get("full_name", ""),
                birth_date=datetime.strptime(self.current_player.get("birth_date", "2000-01-01"), "%Y-%m-%d"),
                team=self.current_player.get("team", ""),
                home_city=self.current_player.get("home_city", ""),
                lineup=self.current_player.get("lineup", ""),
                position=self.current_player.get("position", "")
            ))
            self.current_player = {}

    def characters(self, content):
        if self.current_tag and content.strip():
            self.current_player[self.current_tag] = content.strip()


class FootballModel:
    def __init__(self):
        self.players: List[FootballPlayer] = []
        self._generate_sample_data()

    def _generate_sample_data(self):
        # Генерация 50+ осмысленных записей для демонстрации
        teams = ["Зенит", "Спартак", "ЦСКА", "Динамо", "Локомотив"]
        cities = ["Москва", "Санкт-Петербург", "Казань", "Краснодар"]
        lineups = ["Основной", "Запасной"]
        positions = ["Вратарь", "Защитник", "Полузащитник", "Нападающий"]

        for i in range(1, 51):
            player = FootballPlayer(
                full_name=f"Игрок {i}",
                birth_date=datetime(1990 + (i % 15), (i % 12) + 1, (i % 28) + 1),
                team=teams[i % len(teams)],
                home_city=cities[i % len(cities)],
                lineup=lineups[i % len(lineups)],
                position=positions[i % len(positions)]
            )
            self.players.append(player)

    def add_player(self, player: FootballPlayer):
        self.players.append(player)

    def delete_by_criteria(self, full_name: str = "", birth_date: Optional[datetime] = None,
                           position: str = "", lineup: str = "",
                           team: str = "", home_city: str = "") -> int:
        to_delete = []
        for p in self.players:
            if full_name and full_name.lower() not in p.full_name.lower():
                continue
            if birth_date and p.birth_date != birth_date:
                continue
            if position and p.position.lower() != position.lower():
                continue
            if lineup and p.lineup.lower() != lineup.lower():
                continue
            if team and p.team.lower() != team.lower():
                continue
            if home_city and p.home_city.lower() != home_city.lower():
                continue
            to_delete.append(p)

        count = len(to_delete)
        for p in to_delete:
            self.players.remove(p)
        return count

    def search_by_criteria(self, full_name: str = "", birth_date: Optional[datetime] = None,
                           position: str = "", lineup: str = "",
                           team: str = "", home_city: str = "") -> List[FootballPlayer]:
        result = []
        for p in self.players:
            if full_name and full_name.lower() not in p.full_name.lower():
                continue
            if birth_date and p.birth_date != birth_date:
                continue
            if position and p.position.lower() != position.lower():
                continue
            if lineup and p.lineup.lower() != lineup.lower():
                continue
            if team and p.team.lower() != team.lower():
                continue
            if home_city and p.home_city.lower() != home_city.lower():
                continue
            result.append(p)
        return result

    def save_to_xml(self, filename: str):
        doc = xml.dom.minidom.Document()
        root = doc.createElement("players")
        doc.appendChild(root)
        for player in self.players:
            root.appendChild(player.to_xml_element(doc))

        with open(filename, "w", encoding="utf-8") as f:
            f.write(doc.toprettyxml(indent="  "))

    def load_from_xml(self, filename: str):
        handler = PlayerHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(filename)
        self.players = handler.players