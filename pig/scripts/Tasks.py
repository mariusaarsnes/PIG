import pig.scripts.encryption as e


class Tasks:

    def generate_links(self, key, divisions_created):
        ta_links, student_links = [], []
        for division in divisions_created:
            ta_links.append(self.get_link(key, division.name, division.id, 1))
            student_links.append(self.get_link(key, division.name, division.id, 0))
        return ta_links, student_links

    @classmethod
    def get_link(self, key, division_name, division_id, leader):
        return "apply_group?values=" + e.encode(key, division_name + "," + str(division_id) + "," + str(leader))