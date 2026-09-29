"""Run from any directory with the bundled Python: run_local.py inventory|pilot|plots|tests."""
from pathlib import Path
import argparse
import os
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
sys.path.insert(0,str(ROOT/'.deps'))
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))
os.environ.setdefault('OPENBLAS_NUM_THREADS','2')
os.environ.setdefault('OMP_NUM_THREADS','2')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    actions=('inventory','pilot','validation','heldout','diagnostics','replay_library','replay_train','replay_support','replay_v2','replay_v3','replay_v3_diagnostics','replay_history_probe','replay_v4','replay_calendar_probe','response_strength','replay_mixture','lcl_recovery','lcl_metadata','lcl_census1','lcl_census10','lcl_support','lcl_matching','lcl_anchor_support','lcl_quiet_reference','lcl_response_probe','plots','tests','lcl_validation_intake','lcl_forecast_replay','lcl_forecast_balanced','lcl_information')
    parser.add_argument('action',choices=actions+('lcl_structured_branch','lcl_fixed_response_transfer'))
    args=parser.parse_args()
    source=ROOT/'data/hydro_q/hydro_q_official.csv'
    manifest=ROOT/'reports/hydro_binary_date_split/hydro_event_manifest.json'
    results=ROOT/'results/hydro_train_pilot'
    if args.action=='inventory':
        from cmfir_hydro.metadata import read_rows,build_manifest,source_identity,atomic_json,write_report
        rows,header=read_rows(source);value=build_manifest(rows)
        value['source']=source_identity(source);value['columns']=list(header)
        atomic_json(manifest,value);write_report(value,manifest.parent)
    elif args.action=='pilot':
        from cmfir_hydro.pilot import run
        from cmfir_hydro.compatibility import run as sensitivity
        run(source,manifest,results);sensitivity(results/'pilot_results.json',results)
    elif args.action=='validation':
        from cmfir_hydro.validation import run
        run(source,manifest,results/'pilot_results.json',results/'compatibility_sensitivity.json',ROOT/'results/hydro_validation')
    elif args.action=='heldout':
        from cmfir_hydro.heldout import run
        run(source,manifest,results/'pilot_results.json',ROOT/'results/hydro_validation/validation_results.json',ROOT/'results/hydro_heldout')
    elif args.action=='diagnostics':
        from cmfir_hydro.diagnostics import run
        run(ROOT/'results',ROOT/'results/hydro_diagnostics')
    elif args.action=='replay_library':
        from cmfir_hydro.replay_library import construct
        construct(source,manifest,ROOT/'results/hydro_replay_library')
    elif args.action=='replay_train':
        from cmfir_hydro.replay_train import run
        run(source,manifest,ROOT/'results/hydro_validation/validation_results.json',ROOT/'results/hydro_replay_library/replay_library.json',ROOT/'results/hydro_replay_validation')
    elif args.action=='replay_support':
        from cmfir_hydro.replay_support import audit
        audit(source,ROOT/'results/hydro_replay_library/replay_library.json',ROOT/'results/hydro_replay_v2/support')
    elif args.action=='replay_v2':
        from cmfir_hydro.replay_v2 import run
        run(source,manifest,ROOT/'results/hydro_replay_library/replay_library.json',ROOT/'results/hydro_validation/validation_results.json',ROOT/'results/hydro_replay_v2/experiment')
    elif args.action=='replay_v3':
        from cmfir_hydro.replay_v3 import run
        run(source,manifest,ROOT/'results/hydro_replay_library/replay_library.json',ROOT/'results/hydro_validation/validation_results.json',ROOT/'results/hydro_replay_v3')
    elif args.action=='replay_v3_diagnostics':
        from cmfir_hydro.replay_v3_diagnostics import run
        run(ROOT/'results/hydro_replay_v3')
    elif args.action=='replay_history_probe':
        from cmfir_hydro.replay_history_probe import run
        run(ROOT)
    elif args.action=='replay_v4':
        from cmfir_hydro.replay_v4 import run
        run(ROOT)
    elif args.action=='replay_calendar_probe':
        from cmfir_hydro.replay_calendar_probe import run
        run(ROOT)
    elif args.action=='response_strength':
        from cmfir_hydro.response_strength import run
        run(ROOT)
    elif args.action=='replay_mixture':
        from cmfir_hydro.replay_mixture import run
        run(ROOT)
    elif args.action=='lcl_recovery':
        from cmfir_lcl.recovery_audit import run
        run(ROOT)
    elif args.action=='lcl_metadata':
        from cmfir_lcl.recovery_audit import metadata_inventory
        metadata_inventory(ROOT)
    elif args.action in ('lcl_census1','lcl_census10'):
        from cmfir_lcl.train_census import run
        run(ROOT, 1 if args.action=='lcl_census1' else 10)
    elif args.action=='lcl_support':
        from cmfir_lcl.support_census import run
        run(ROOT)
    elif args.action=='lcl_matching':
        from cmfir_lcl.matching_probe import run
        run(ROOT)
    elif args.action=='lcl_anchor_support':
        from cmfir_lcl.anchor_support import run
        run(ROOT)
    elif args.action=='lcl_quiet_reference':
        from cmfir_lcl.quiet_reference import run
        run(ROOT)
    elif args.action=='lcl_response_probe':
        from cmfir_lcl.response_probe import run
        run(ROOT)
    elif args.action=='lcl_validation_intake':
        from cmfir_lcl.validation_intake import run
        run(ROOT)
    elif args.action in ('lcl_forecast_replay','lcl_forecast_balanced'):
        from cmfir_lcl.forecast_replay import run
        run(ROOT,phase_balanced=args.action=='lcl_forecast_balanced')
    elif args.action=='lcl_information':
        from cmfir_lcl.information import run
        run(ROOT)
    elif args.action=='lcl_structured_branch':
        from cmfir_lcl.structured_branch import run
        run(ROOT)
    elif args.action=='lcl_fixed_response_transfer':
        from cmfir_lcl.fixed_response_transfer import run
        run(ROOT)
    elif args.action=='plots':
        from cmfir_hydro.plots import build
        build(manifest,results)
    else:
        suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'))
        outcome=unittest.TextTestRunner(verbosity=2).run(suite)
        raise SystemExit(0 if outcome.wasSuccessful() else 1)


if __name__=='__main__':
    main()
