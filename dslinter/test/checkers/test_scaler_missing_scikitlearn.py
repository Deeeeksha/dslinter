import astroid

import dslinter.plugin
import pylint.testutils


class TestScalerMissingScikitLearn(pylint.testutils.CheckerTestCase):

    CHECKER_CLASS = dslinter.plugin.ScalerMissingScikitLearnChecker

    # def test_PCA_missing_scaling(self):
    #     node = astroid.extract_node("""
    #         from sklearn.datasets import load_wine
    #         from sklearn.model_selection import train_test_split
    #         from sklearn.pipeline import make_pipeline
    #         from sklearn.decomposition import PCA
    #         from sklearn.naive_bayes import GaussianNB
    #         from sklearn.metrics import accuracy_score
    #
    #         RANDOM_STATE = 42
    #         features, target = load_wine(return_X_y=True)
    #         X_train, X_test, y_train, y_test = train_test_split(
    #             features, target, test_size=0.30, random_state=RANDOM_STATE
    #         )
    #         clf = make_pipeline(PCA(n_components=2), GaussianNB()) #@
    #         clf.fit(X_train, y_train)
    #         pred_test = clf.predict(X_test)
    #         ac = accuracy_score(y_test, pred_test)
    #     """)
    #     with self.assertAddsMessages(
    #         pylint.testutils.MessageTest(
    #             msg_id= 'scaler-missing-scikitlearn',
    #             node = node,
    #         )
    #     ):
    #         self.checker.visit_call(node)

    def test_PCA_with_scaling(self):
        node = astroid.extract_node("""
            from sklearn.datasets import load_wine
            from sklearn.model_selection import train_test_split
            from sklearn.pipeline import make_pipeline
            from sklearn.decomposition import PCA
            from sklearn.naive_bayes import GaussianNB
            from sklearn.metrics import accuracy_score
            from sklearn.preprocessing import StandardScaler

            RANDOM_STATE = 42
            features, target = load_wine(return_X_y=True)
            X_train, X_test, y_train, y_test = train_test_split(
                features, target, test_size=0.30, random_state=RANDOM_STATE
            )
            clf = make_pipeline(StandardScaler(), PCA(n_components=2), GaussianNB()) #@
            clf.fit(X_train, y_train)
            pred_test = clf.predict(X_test)
            ac = accuracy_score(y_test, pred_test)
        """)
        with self.assertNoMessages():
            self.checker.visit_call(node)

    # def test_SVC_missing_scaling(self):
    #     node = astroid.extract_node("""
    #         from sklearn.datasets import load_wine
    #         from sklearn.model_selection import train_test_split
    #         from sklearn.pipeline import make_pipeline
    #         from sklearn.decomposition import PCA
    #         from sklearn.naive_bayes import GaussianNB
    #         from sklearn.metrics import accuracy_score
    #         from sklearn.preprocessing import StandardScaler
    #
    #         RANDOM_STATE = 42
    #         features, target = load_wine(return_X_y=True)
    #         X_train, X_test, y_train, y_test = train_test_split(
    #             features, target, test_size=0.30, random_state=RANDOM_STATE
    #         )
    #         clf = make_pipeline(StandardScaler(), PCA(n_components=2), GaussianNB()) #@
    #         clf.fit(X_train, y_train)
    #         pred_test = clf.predict(X_test)
    #         ac = accuracy_score(y_test, pred_test)
    #     """)
    #     with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id='scaler-missing-scikitlearn', node = node)):
    #         self.checker.visit_call(node)
    #
    #
    # def test_SVC_with_scaling(self):
    #     node = astroid.extract_node("""
    #         from sklearn.datasets import load_wine
    #         from sklearn.model_selection import train_test_split
    #         from sklearn.pipeline import make_pipeline
    #         from sklearn.decomposition import PCA
    #         from sklearn.naive_bayes import GaussianNB
    #         from sklearn.metrics import accuracy_score
    #         from sklearn.preprocessing import StandardScaler
    #
    #         RANDOM_STATE = 42
    #         features, target = load_wine(return_X_y=True)
    #         X_train, X_test, y_train, y_test = train_test_split(
    #             features, target, test_size=0.30, random_state=RANDOM_STATE
    #         )
    #         clf = make_pipeline(StandardScaler(), PCA(n_components=2), GaussianNB()) #@
    #         clf.fit(X_train, y_train)
    #         pred_test = clf.predict(X_test)
    #         ac = accuracy_score(y_test, pred_test)
    #     """)
    #     with self.assertNoMessages():
    #         self.checker.visit_call(node)
