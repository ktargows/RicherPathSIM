import cPickle
import os
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.barebones.Helper import  getMetaPathAdjacencyData, findMostSimilarNodes, testAuthors

__author__ = 'jontedesco'

class AuthorsPathSimAPPAExperiment(Experiment):
    """
      Runs some experiments with NeighborSim on author similarity for the 'four area' dataset
    """

    def runFor(self, author, adjMatrix, extraData, citationCounts, publicationCounts):
        print("Running for %s..." % author)

        # Find the top 10 most similar nodes to some given node
        mostSimilar, similarityScores = findMostSimilarNodes(adjMatrix, author, extraData)
        self.output('\nMost Similar to "%s":' % author)
        mostSimilarTable = texttable.Texttable()
        rows = [['Author', 'Score', 'Citations', 'Publications']]
        rows += [[name, score, citationCounts[name], publicationCounts[name]] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        self.output(mostSimilarTable.draw())

        # Output all similarity scores
        outputPath = os.path.join('results', 'authors', 'intermediate', '%s-pathsim-appa' % author.replace(' ', ''))
        cPickle.dump(similarityScores, open(outputPath, 'wb'))

def run(citationCounts, publicationCounts):
    experiment = AuthorsPathSimAPPAExperiment(
        None,
        'Most Similar APPA PathSim Authors',
        outputFilePath = os.path.join('results','authors','appaPathSim')
    )

    # Compute once, since these never change
    graph, nodeIndex = cPickle.load(open(os.path.join('data', 'graphWithCitations')))
    appaAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['author', 'paper', 'paper', 'author'])

    # Run for all authors
    for testAuthor in testAuthors:
        experiment.runFor(testAuthor, appaAdjMatrix, extraData, citationCounts, publicationCounts)