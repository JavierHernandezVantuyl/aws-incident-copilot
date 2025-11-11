"""Tests for incident models."""

import pytest
from copilot.incidents import Incident


def test_incident_creation():
    """Test creating an incident."""
    incident = Incident(
        id="test-incident",
        title="Test Incident",
        severity="HIGH",
        resource="i-12345",
        description="This is a test incident",
        suggested_fix="Fix it",
        evidence_files=["file1.json", "file2.json"],
    )

    assert incident.id == "test-incident"
    assert incident.title == "Test Incident"
    assert incident.severity == "HIGH"
    assert incident.resource == "i-12345"
    assert len(incident.evidence_files) == 2


def test_incident_minimal():
    """Test creating incident with minimal fields."""
    incident = Incident(
        id="minimal",
        title="Minimal",
        severity="LOW",
        resource="resource-1",
        description="Description",
        suggested_fix="Fix",
    )

    assert incident.id == "minimal"
    assert incident.evidence_files == []


def test_incident_serialization():
    """Test incident serialization."""
    incident = Incident(
        id="test",
        title="Test",
        severity="MEDIUM",
        resource="test-resource",
        description="Test description",
        suggested_fix="Test fix",
    )

    # Test model_dump
    data = incident.model_dump()
    assert data["id"] == "test"
    assert data["severity"] == "MEDIUM"
    assert "evidence_files" in data


def test_incident_from_dict():
    """Test creating incident from dictionary."""
    data = {
        "id": "from-dict",
        "title": "From Dict",
        "severity": "CRITICAL",
        "resource": "arn:aws:s3:::bucket",
        "description": "Test",
        "suggested_fix": "Fix",
        "evidence_files": [],
    }

    incident = Incident(**data)
    assert incident.id == "from-dict"
    assert incident.severity == "CRITICAL"
