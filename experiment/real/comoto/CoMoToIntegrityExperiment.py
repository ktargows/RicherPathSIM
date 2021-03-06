import os
from experiment.Experiment import Experiment
from src.experiment.helper import ExperimentHelper
from src.model.node.comoto.Assignment import Assignment
from src.model.node.comoto.Semester import Semester
from src.model.node.comoto.Submission import Submission

__author__ = 'jontedesco'

class CoMoToIntegrityExperiment(Experiment):

    def run(self):

        assignmentData = {}

        experimentHelper = ExperimentHelper()

        # Print the semesters with submissions & the number of submissions for each
        for node in self.graph.getNodes():
            if isinstance(node, Assignment):

                node.submissionCount = 0
                semester = None
                for otherNode in self.graph.getSuccessors(node):
                    if isinstance(otherNode , Submission):
                        node.submissionCount += 1
                    elif isinstance(otherNode, Semester):
                        semester = otherNode

                if semester not in assignmentData:
                    assignmentData[semester] = []

                assignmentData[semester].append(node)

        # Order by calendar dates
        keys = sorted(assignmentData.keys(), key=lambda s: (s.year, ('Spring', 'Summer', 'Fall').index(s.season)))

        for semester in keys:
            nodes = assignmentData[semester]
            for node in nodes:

                # Output the name of the assignment & number of submissions we have for it
                self.output("%s (%s %d):  %d" % (node.name, semester.season, semester.year, node.submissionCount))

        # Output the assignments & semesters included
        self.output("\n\nSemesters Included:\n")
        for semester in experimentHelper.getNodesByType(self.graph, Semester):
            self.output("%s %d" % (semester.season, semester.year))
        self.output("\n\nAssignments Included:\n")
        for assignment in experimentHelper.getNodesByType(self.graph, Assignment):
            self.output("%s" % assignment.name)


if __name__ == '__main__':
    experiment = CoMoToIntegrityExperiment(
        os.path.join('graphs', 'cs225comotodata'),
        'CoMoTo data integrity experiment',
    )
    experiment.start()

    experiment = CoMoToIntegrityExperiment(
        os.path.join('graphs', 'cs225comotodata-pruned'),
        'CoMoTo data integrity experiment'
    )
    experiment.start()