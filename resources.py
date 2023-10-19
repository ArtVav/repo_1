import json
import os


def print_with_indent(value, indent=0):
    indentation = '\t' * indent
    print(f'{indentation}{value}')


class Entry:
    def __init__(self, title, entries=None, parent=None):
        self.title = title
        if entries is None:
            entries = []
        self.entries = entries
        self.parent = parent

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent=indent + 1)

    def __str__(self):
        return self.title

    @classmethod
    def from_json(cls, entries_dict: dict):
        entry_json = cls(entries_dict['title'])
        for entries_dict in entries_dict.get('entries', []):
            entry_json.add_entry(cls.from_json(entries_dict))
        return entry_json

    def json(self):
        res = {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries]
        }
        return res

    def save(self, path):
        content = self.json()
        with open(path + '/' + f'{self.title}.json', 'w', encoding='utf-8') as f:
            json.dump(content, f)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = json.load(f)
            return Entry.from_json(content)


class EntryManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.entries = []

    def load(self):
        if not os.path.isdir(self.data_path):
            os.makedirs(self.data_path)
        else:
            for filename in os.listdir(self.data_path):
                if filename.endswith('json'):
                    entry = Entry.load(os.path.join(self.data_path, filename))
                    self.entries.append(entry)
        return self

    def add_entry(self, title):
        self.entries.append(Entry(title))

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)