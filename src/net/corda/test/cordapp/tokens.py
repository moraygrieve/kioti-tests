from pysys.utils.filecopy import filecopy
from net.corda.test.constants import *
from net.corda.test.cordapp.sshclient import CorDappSSHClient
from net.corda.test.distribution.artifact import getMidStackArtifact

class TokensCorDapp():
    """Utility class around the Tokens SDK only Test CorDapp application."""

    @classmethod
    def copyjars(cls, toDir):
        jars = [os.path.join(CORDAPPS_DIR, 'tokens', 'staging', 'tokens-test-cordapp-workflows.jar')]
        map(lambda x: filecopy(x, os.path.join(toDir, os.path.basename(x))), jars)
        map(lambda x: filecopy(x, os.path.join(toDir, os.path.basename(x))), cls.getjars())

    @classmethod
    def getjars(cls):
        tw = getMidStackArtifact(TOKENS_SDK_VERSION, 'tokens-workflows')
        tm = getMidStackArtifact(TOKENS_SDK_VERSION, 'tokens-money')
        ts = getMidStackArtifact(TOKENS_SDK_VERSION, 'tokens-selection')
        tc = getMidStackArtifact(TOKENS_SDK_VERSION, 'tokens-contracts')
        return (tw, tm, ts, tc)


class TokensSSHClient(CorDappSSHClient):
    """Abstraction over ssh command interaction with the Tokens SDK only Test CorDapp."""

    def issueCash(self, node, issueTo, amount=10, timeout=None, stdout=None, stderr=None, logOut=True):
        """Run a flow to issue tokens from to another node.

        :param node: The node acting as the issuer
        :param issueTo: The node to issue to
        :param amount: The amount to issue (defaults 10)
        :param timeout: The timeout on the flow command
        :param stdout: Filename for stdout
        :param stderr: Filename for stderr
        :return:
        """
        fstdout = os.path.join(node.directory, 'issue-cash.out' if stdout is None else stdout)
        fstderr = os.path.join(node.directory, 'issue-cash.err' if stderr is None else stderr)
        command = 'flow start IssueCash issueTo: "%s", amount: "%d"' % (issueTo.config.myLegalName, amount)
        if logOut: self.log.info('Performing ssh command: %s' % command)
        self.createClient(node, fstdout, fstderr).execute(command, timeout).close()


    def selectCash(self, node, amount=10, printSelected=True, localSelector=False, timeout=None, stdout=None, stderr=None):
        """Run a flow to query tokens.

        :param node: The node to run the flow on
        :param amount: The amount requested  in the selection (defaults 10)
        :param printSelected: If true print out details of the selected tokens
        :param localSelector: If true use local token selector (otherwise use database)
        :param timeout: The timeout on the flow command
        :param stdout: Filename for stdout
        :param stderr: Filename for stderr
        :return:
        """
        fstdout = os.path.join(node.directory, 'select-cash.out' if stdout is None else stdout)
        fstderr = os.path.join(node.directory, 'select-cash.err' if stderr is None else stderr)
        command = 'flow start SelectCash amount: "%d", print: %s, local: %s' % (amount, printSelected, localSelector)
        self.log.info('Performing ssh command: %s' % command)
        self.createClient(node, fstdout, fstderr).execute(command, timeout).close()


    def moveCash(self, node, moveTo, amount=10, timeout=None, stdout=None, stderr=None):
        """Run a flow to query tokens.

        :param node: The node to run the flow on
        :param moveTo: The node to move the tokens to
        :param amount: The amount requested  in the selection (defaults 10)
        :param timeout: The timeout on the flow command
        :param stdout: Filename for stdout
        :param stderr: Filename for stderr
        :return:
        """
        fstdout = os.path.join(node.directory, 'move-cash.out' if stdout is None else stdout)
        fstderr = os.path.join(node.directory, 'move-cash.err' if stderr is None else stderr)
        command = 'flow start MoveCash moveTo: "%s", amount: "%d"' % (moveTo.config.myLegalName, amount)
        self.log.info('Performing ssh command: %s' % command)
        self.createClient(node, fstdout, fstderr).execute(command, timeout).close()


    def queryFungibleToken(self, node, timeout=None, stdout='query-fungible.out', stderr='query-fungible.err'):
        """Perform a vault query for a FungibleToken.

        :param node: The node to execute the vault query on
        :param timeout: The timeout for the transaction
        :param stdout: Filename to store any stdout from running the command
        :param stderr: Filename to store any stderr from running the command
        """
        self.vaultQuery(node, contractStateType='com.r3.corda.lib.tokens.contracts.states.FungibleToken', timeout=timeout, stdout=stdout, stderr=stderr)
