import mock

from tornado.httpclient import AsyncHTTPClient
from tornado.testing import AsyncTestCase

from ..client import AsyncGitHubClient


class GithubClientTest(AsyncTestCase):
    def setUp(self):
        super(GithubClientTest, self).setUp()
        self.http_client = mock.create_autospec(AsyncHTTPClient)
        with mock.patch('os.environ.get', return_value='https://api.github.com/'):
            self.gh_client = AsyncGitHubClient(client=self.http_client)

    def _get_url(self):
        args, kw = self.http_client.fetch.call_args
        return args[0]

    def assertStartsWith(self, string, beginning):
        self.assertTrue(string.startswith(beginning),
                        '%s does not start with %s' % (string, beginning))

    def test_basic_fetch(self):
        self.gh_client.fetch('https://api.github.com/url')
        self.assertTrue(self.http_client.fetch.called)

    def test_fetch_params(self):
        params = {'unique_param_name': 1}
        self.gh_client.fetch('https://api.github.com/url', params=params)
        url = self._get_url()
        self.assertTrue('unique_param_name' in url)

    def test_log_rate_limit(self):
        pass

    def test_get_repos(self):
        self.gh_client.get_repos('username')
        url = self._get_url()
        self.assertStartsWith(url, 'https://api.github.com/users/username/repos')

    def test_get_contents(self):
        user = 'username'
        repo = 'my_awesome_repo'
        path = 'more-path'
        self.gh_client.get_contents(user, repo, path)
        url = self._get_url()
        correct_url = 'https://api.github.com/repos/username/my_awesome_repo/contents/more-path'
        self.assertStartsWith(url, correct_url)

    def test_get_branches(self):
        user = 'username'
        repo = 'my_awesome_repo'
        self.gh_client.get_branches(user, repo)
        url = self._get_url()
        correct_url = 'https://api.github.com/repos/username/my_awesome_repo/branches'
        self.assertStartsWith(url, correct_url)

    def test_get_tags(self):
        user = 'username'
        repo = 'my_awesome_repo'
        self.gh_client.get_tags(user, repo)
        url = self._get_url()
        correct_url = 'https://api.github.com/repos/username/my_awesome_repo/tags'
        self.assertStartsWith(url, correct_url)

    def test_get_tree_entry(self):
        user = 'username'
        repo = 'my_awesome_repo'
        path = 'extra-path'
        self.gh_client.get_tree_entry(user, repo, path)
        url = self._get_url()
        correct_url = 'https://api.github.com/repos/username/my_awesome_repo/git/trees/extra-path'
        self.assertStartsWith(url, correct_url)

    def test_get_gist(self):
        gist_id = 'ap90avn23iovv2ovn2309n'
        self.gh_client.get_gist(gist_id)
        url = self._get_url()
        correct_url = 'https://api.github.com/gists/' + gist_id
        self.assertStartsWith(url, correct_url)

    def test_get_gists(self):
        user = 'username'
        self.gh_client.get_gists(user)
        url = self._get_url()
        correct_url = 'https://api.github.com/users/username/gists'
        self.assertStartsWith(url, correct_url)
