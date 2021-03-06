# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialManager_revert_to_repository_01():

    wrangler = score_manager._material_package_wrangler
    manager = wrangler._find_up_to_date_manager(
        repository='git',
        system=True,
        )

    assert manager._test_revert_to_repository()
    

def test_MaterialManager_revert_to_repository_02():

    wrangler = score_manager._material_package_wrangler
    manager = wrangler._find_up_to_date_manager(
        repository='svn',
        system=False,
        )
            
    if not manager:
        return

    assert manager._test_revert_to_repository()