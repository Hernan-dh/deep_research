import unittest
from unittest.mock import patch

import app


class DownloadFlowTests(unittest.IsolatedAsyncioTestCase):
    async def test_report_is_downloadable_only_after_successful_completion(self):
        class Manager:
            async def run(self, *args):
                yield "Planning"
                yield "# Final report"

        with patch.object(app, "ResearchManager", Manager):
            updates = [value async for value in app.run("Example", [], "English")]
        self.assertTrue(all(value[1] is None for value in updates[:-1]))
        self.assertEqual(updates[-1][1], "# Final report")

    async def test_failure_never_exports_partial_status(self):
        class Manager:
            async def run(self, *args):
                yield "Planning"
                raise RuntimeError("simulated outage")

        with patch.object(app, "ResearchManager", Manager), patch.object(app.traceback, "print_exc"):
            updates = [value async for value in app.run("Example", [], "English")]
        self.assertTrue(all(value[1] is None for value in updates))
        self.assertIn("couldn't", updates[-1][0])
