"""Einstiegspunkt der Anwendung."""

from controllers.dashboard_controller import DashboardController
from repositories.student_repository import PickleStudentRepository
from services.studium_service import StudiumService
from views.cmd_dashboard_view import CmdDashboardView


def main() -> None:
    """Initialisiert die Architektur-Schichten und startet die Anwendung."""
    # Datenzugriffsschicht
    repository = PickleStudentRepository()

    # Geschäftslogik-Schicht
    service = StudiumService(repository)

    # Steuerungsschicht
    controller = DashboardController(service)

    # Präsentationsschicht
    view = CmdDashboardView(controller)

    # App starten
    view.start_routine()


if __name__ == "__main__":
    main()
