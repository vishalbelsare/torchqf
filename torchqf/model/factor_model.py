import torch
from torch.nn import Module


class FactorModel(Module):
    """
    Factor model.

    Parameters
    ----------
    factors : Tensor

    Attributes
    ----------
    beta : Tensor
        Created after `fit`.

    Shape
    -----
    input : :math:`(*, A, T)`
        :math:`A` is the number of assets.
        :math:`T` is the number of time steps.
    output : :math:`(*, A, T)`
        :math:`A` is the number of assets.
        :math:`T` is the number of time steps.
    factors : :math:`(*, F, T)`
        :math:`F` is the number of assets.
        :math:`T` is the number of time steps.
    beta : :math:`(F, A)`
        :math:`F` is the number of factors.
        :math:`A` is the number of assets.

    Examples
    --------
    >>> import torchqf
    >>> from torchqf.stochastic import generate_brownian

    >>> _ = torch.manual_seed(42)

    >>> input = generate_brownian((2, 5), 0.1)
    >>> factors = generate_brownian((2, 5), 0.1)
    >>> fm = FactorModel().fit(input, factors)
    >>> fm(input, factors)
    tensor([[ 0.0032, -0.0023, -0.0046,  0.0138, -0.0099],
            [-0.0234,  0.0157, -0.0017, -0.0052,  0.0025]])

    The method `fit_forward` fits and forwards at once.

    >>> fm.fit_forward(input, factors)
    tensor([[ 0.0032, -0.0023, -0.0046,  0.0138, -0.0099],
            [-0.0234,  0.0157, -0.0017, -0.0052,  0.0025]])
    """

    def __init__(self):
        super().__init__()

    def fit(self, input, factors):
        """
        Fit the model using the asset returns (`input`)
        and the factor returns (`factors`).

        Shape
        -----
        input : :math:`(*, A, T)`
            :math:`A` is the number of assets.
            :math:`T` is the number of time steps.
        factors : :math:`(*, F, T)`
            :math:`F` is the number of assets.
            :math:`T` is the number of time steps.
        beta : :math:`(*, F, A)`
            :math:`F` is the number of factors.
            :math:`A` is the number of assets.
        """
        assert input.size(-1) == factors.size(-1), "numbers of time steps do not match"
        assert input.ndim == 2, "not supported"
        assert factors.ndim == 2, "not supported"

        X = factors.t()  # shape : (T, F)
        y = input.transpose(-2, -1)  # shape : (T, A)

        # Compute beta : (F, T) @ (T, A) = (F, A)
        beta = torch.mm(torch.linalg.pinv(X), y)

        self.beta = beta

        return self

    def forward(self, input: torch.Tensor, factors: torch.Tensor) -> torch.Tensor:
        factor_return = torch.mm(self.beta.t(), factors)  # shape : (*, A, T)
        return input - factor_return

    def fit_forward(self, input: torch.Tensor, factors: torch.Tensor) -> torch.Tensor:
        return self.fit(input, factors)(input, factors)
