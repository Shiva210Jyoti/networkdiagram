import pytest
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from networkdiagram import CriticalPathMethod


def test_generate_gantt_chart_basic(monkeypatch):
    """Test generating a Gantt chart with explicit activities does not crash."""
    monkeypatch.setattr(plt, "show", lambda: None)
    
    cpm = CriticalPathMethod()
    cpm.add_activity('O', 0)
    cpm.add_activity('A', 3)
    cpm.add_activity('B', 4)
    cpm.add_relation('A', '-')
    cpm.add_relation('B', 'A')
    
    # Call without show=False to test the mocked plt.show and default parameter
    cpm.generate_gantt_chart()
    
    # Calculations should have been triggered automatically
    assert cpm.total_project_duration == 7
    assert 'A' in cpm.critical_path
    assert 'B' in cpm.critical_path


def test_generate_gantt_chart_empty(capsys):
    """Test generating a chart with no activities."""
    cpm = CriticalPathMethod()
    cpm.generate_gantt_chart(show=False)
    
    captured = capsys.readouterr()
    assert "No activities to display" in captured.out


def test_generate_gantt_chart_single_activity():
    """Test generating a chart with a single activity."""
    cpm = CriticalPathMethod()
    cpm.add_activity('O', 0)
    cpm.add_activity('A', 5)
    cpm.add_relation('A', '-')
    
    cpm.generate_gantt_chart(show=False)
    
    assert cpm.total_project_duration == 5
    assert 'A' in cpm.critical_path


def test_generate_gantt_chart_with_float():
    """Test generating a chart for a network with float/slack."""
    cpm = CriticalPathMethod()
    cpm.add_activity('O', 0)
    cpm.add_activity('A', 3)
    cpm.add_activity('B', 2)
    cpm.add_activity('C', 5)
    
    cpm.add_relation('A', '-')
    cpm.add_relation('B', 'A')
    cpm.add_relation('C', 'A')  # B and C run in parallel
    
    cpm.generate_gantt_chart(show=False)
    
    # Path O-A-C is 0+3+5 = 8
    # Path O-A-B is 0+3+2 = 5
    # C is critical, B has float of 3
    assert cpm.total_project_duration == 8
    assert 'C' in cpm.critical_path
    assert 'B' not in cpm.critical_path
    assert (cpm.nodes['B'].latest_finish - cpm.nodes['B'].early_finish) == 3


def test_generate_gantt_chart_pre_calculated():
    """Test generating a chart when calculations are already done."""
    cpm = CriticalPathMethod()
    cpm.add_activity('A', 2)
    cpm.add_relation('A', '-')
    
    cpm.find_probable_paths()
    cpm.find_critical_path()
    cpm.forward_pass()
    cpm.backward_pass()
    
    # Should not re-run calculations but use existing
    cpm.generate_gantt_chart(show=False)
    assert cpm.total_project_duration == 2
