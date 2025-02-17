"""Checker checks whether scaler is added before scaling-sensitive operations."""
import traceback
from typing import List
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from dslinter.util.exception_handler import ExceptionHandler
from dslinter.util.ast import AssignUtil


class ScalerMissingScikitLearnChecker(BaseChecker):
    """Checker checks whether scaler is added before scaling-sensitive operations."""

    __implements__ = IAstroidChecker

    name = "pca-scaler"
    priority = -1
    msgs = {
        "W5508": (
            "Scaler is not used before PCA",
            "scaler-missing-scikitlearn",
            "To ensure a good result, use feature scaling before Principle Component Analysis."
        ),
    }
    options = ()

    PIPELINE = [
        "make_pipeline",
        "Pipeline",
    ]

    PCA = ["PCA", "KernelPCA", "SparsePCA", "IncrementalPCA", "SVC"]

    SCALER = ["RobustScaler", "StandardScaler", "MaxAbsScaler", "MinMaxScaler",]

    LEARNING_FUNCTIONS: List[str] = [
        "fit",
        "fit_transform",
        "transform",
    ]

    Variables = []


    def visit_call(self, node: astroid.Call):
        """
        When a node is visited, add a message if the rule is violated.
        :param node:
        :return:
        """
        try:
            # If there is no scaler before a pca, the rule is violated.
            if (
                hasattr(node, "func")
                and node.func is not None
                and hasattr(node.func, "name")
                and node.func.name in self.PIPELINE
                and node.args is not None
            ):
                has_pca = False
                has_scaler = False
                for arg in node.args:
                    if isinstance(arg, astroid.Call):
                        if ScalerMissingScikitLearnChecker._call_initiates_scaler(arg):
                            has_scaler = True
                        if ScalerMissingScikitLearnChecker._call_initiates_pca(arg):
                            has_pca = True
                            break
                    if isinstance(arg, astroid.node_classes.List):
                        for kid in arg.get_children():
                            for item in kid.get_children():
                                if isinstance(item, astroid.Call):
                                    if ScalerMissingScikitLearnChecker._call_initiates_scaler(item):
                                        has_scaler=True
                                    if ScalerMissingScikitLearnChecker._call_initiates_pca(item):
                                        has_pca=True
                            if has_pca is True:
                                break
                if has_pca is True and has_scaler is False:
                    self.add_message("pca scaler checker", node=node)

            if (
                    hasattr(node, "func")
                    and node.func is not None
                    and hasattr(node.func, "attrname")
                    and node.func.attrname in self.LEARNING_FUNCTIONS
                    and self._expr_is_pca(node.func.expr)
                    and node.args is not None
            ):
                has_pca = True
                has_scaler = False
                for arg in node.args:
                    if isinstance(arg, astroid.Name):
                        values = AssignUtil.assignment_values(arg)
                        for value in values:
                            if (
                                    isinstance(value, astroid.Call)
                                    and value.func is not None
                                    and hasattr(value.func, "attrname")
                                    and value.func.attrname in self.LEARNING_FUNCTIONS
                            ):
                                if self._expr_is_scaler(value.func.expr):
                                    has_scaler = True
                                elif(isinstance(value.func.expr, astroid.Call)
                                    and value.func.expr.func is not None
                                    and hasattr(value.func.expr.func, "attrname")
                                    and value.func.expr.func.attrname in self.LEARNING_FUNCTIONS
                                    and self._expr_is_scaler(value.func.expr.func.expr)
                                ):
                                    has_scaler = True
                if has_pca is True and has_scaler is False:
                    self.add_message("pca scaler checker", node=node)


        except:  # pylint: disable=bare-except
            ExceptionHandler.handle(self, node)
            traceback.print_exc()

    @staticmethod
    def _call_initiates_pca(call: astroid.Call) -> bool:
        """
        Evaluate whether a Call node is initiating an pca.

        :param call: Call to evaluate.
        :return: True when an estimator is initiated.
        """
        return (
                call.func is not None
                and hasattr(call.func, "name")
                and call.func.name in ScalerMissingScikitLearnChecker.PCA
        )

    @staticmethod
    def _call_initiates_scaler(call: astroid.Call) -> bool:
        """
        Evaluate whether a Call node is initiating an scaler.

        :param call: Call to evaluate.
        :return: True when an estimator is initiated.
        """
        return (
                call.func is not None
                and hasattr(call.func, "name")
                and call.func.name in ScalerMissingScikitLearnChecker.SCALER
        )

    @staticmethod
    def _expr_is_pca(expr: astroid.node_classes.NodeNG) -> bool:
        """
        Evaluate whether the expression is an estimator.

        :param expr: Expression to evaluate.
        :return: True when the expression is an estimator.
        """
        if isinstance(expr, astroid.Call) and ScalerMissingScikitLearnChecker._call_initiates_pca(expr):
            return True

        # If expr is a Name, check whether that name is assigned to an estimator.
        if isinstance(expr, astroid.Name):
            values = AssignUtil.assignment_values(expr)
            for value in values:
                if ScalerMissingScikitLearnChecker._expr_is_pca(value):
                    return True
        return False

    @staticmethod
    def _expr_is_scaler(expr: astroid.node_classes.NodeNG) -> bool:
        """
        Evaluate whether the expression is an estimator.

        :param expr: Expression to evaluate.
        :return: True when the expression is an estimator.
        """
        if isinstance(expr, astroid.Call) and ScalerMissingScikitLearnChecker._call_initiates_scaler(expr):
            return True

        # If expr is a Name, check whether that name is assigned to an estimator.
        if isinstance(expr, astroid.Name):
            values = AssignUtil.assignment_values(expr)
            for value in values:
                if ScalerMissingScikitLearnChecker._expr_is_scaler(value):
                    return True
        return False
