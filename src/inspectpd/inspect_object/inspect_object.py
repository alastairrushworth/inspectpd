"""The DataFrame subclass returned by every ``inspect_*`` summary."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, ClassVar

from pandas import DataFrame


class InspectFrame(DataFrame):
    """A :class:`pandas.DataFrame` that remembers which summary produced it.

    Two pieces of metadata travel with the frame through ordinary pandas
    operations (slicing, sorting, ``head()``, ``copy()`` and so on):

    ``inspect_type``
        The name of the summary function that produced the frame, for
        example ``"inspect_cat"``. :meth:`view` uses it to pick a plot.
    ``inspect_params``
        A dict of the parameters the summary was computed with, so that
        :meth:`view` can stay consistent with them (for example the ``alpha``
        used for correlation confidence intervals).
    """

    _metadata: ClassVar[list[str]] = ["inspect_type", "inspect_params"]

    def __init__(
        self,
        *args: Any,
        inspect_type: str | None = None,
        inspect_params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        self.inspect_type = inspect_type
        self.inspect_params = dict(inspect_params or {})
        super().__init__(*args, **kwargs)

    @property
    def _constructor(self) -> Callable[..., InspectFrame]:
        def _from_parts(*args: Any, **kwargs: Any) -> InspectFrame:
            return InspectFrame(*args, **kwargs).__finalize__(self)

        return _from_parts

    def view(self, **kwargs: Any) -> Any:
        """Visualise the summary as a plotnine ``ggplot`` object.

        Parameters
        ----------
        **kwargs
            Passed through to the plotting function for this summary type.
            ``inspect_cat`` accepts ``high_cardinality`` (int): pool levels
            that occur this many times or fewer into a single
            "High cardinality" block. ``inspect_cor`` accepts ``max_pairs``
            (int or None): the maximum number of column pairs to draw.

        Returns
        -------
        plotnine.ggplot
            Displays automatically in a notebook. In a script or REPL call
            ``.show()`` on it, or ``.save("plot.png")``.

        Raises
        ------
        ValueError
            If the summary is empty, or the frame's summary type is unknown.
        """
        # plotnine (and matplotlib behind it) are imported lazily so that
        # ``import inspectpd`` stays cheap when no plots are drawn.
        from inspectpd.view.view_cat import view_cat
        from inspectpd.view.view_cor import view_cor
        from inspectpd.view.view_imb import view_imb
        from inspectpd.view.view_mem import view_mem
        from inspectpd.view.view_na import view_na
        from inspectpd.view.view_num import view_num
        from inspectpd.view.view_types import view_types

        plotters: dict[str, Callable[..., Any]] = {
            "inspect_cat": view_cat,
            "inspect_cor": view_cor,
            "inspect_imb": view_imb,
            "inspect_mem": view_mem,
            "inspect_na": view_na,
            "inspect_num": view_num,
            "inspect_types": view_types,
        }
        plotter = plotters.get(self.inspect_type or "")
        if plotter is None:
            valid = ", ".join(sorted(plotters))
            raise ValueError(
                f"cannot view a frame with inspect_type={self.inspect_type!r}; "
                f"expected one of: {valid}"
            )
        return plotter(self, **kwargs)


# Backwards-compatible alias for the previous (lowercase) class name.
inspect_object = InspectFrame
