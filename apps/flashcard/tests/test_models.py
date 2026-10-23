from types import ModuleType

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError

import pytest

from apps.users.models import User

from ..models import Deck, Word

pytestmark = pytest.mark.django_db


def test_shared_words_keep_progress_after_deck_deletion(
    card_models: ModuleType,
    learner: User,
    word: Word,
    deck: Deck,
):
    """Deleting one deck preserves shared words and their latest grades."""
    other = card_models.Deck.objects.create(title="Travel", level="A2")
    card_models.DeckWord.objects.create(deck=deck, word=word, position=0)
    card_models.DeckWord.objects.create(deck=other, word=word, position=0)
    progress = card_models.WordProgress.objects.create(
        user=learner,
        word=word,
        status="known",
    )
    card_models.Bookmark.objects.create(user=learner, deck=deck)
    state = card_models.UserLearningState.objects.create(
        user=learner,
        last_deck=deck,
    )
    deck.delete()
    state.refresh_from_db()
    progress.refresh_from_db()
    assert state.last_deck is None
    assert progress.status == "known"
    assert list(other.words.all()) == [word]
    assert card_models.DeckWord.objects.count() == 1
    assert not card_models.Bookmark.objects.exists()


def test_memberships_are_ordered(
    card_models: ModuleType,
    deck: Deck,
    word: Word,
):
    """Membership queries follow display order rather than insertion order."""
    second = card_models.Word.objects.create(
        english="bye",
        vietnamese="tạm biệt",
    )
    card_models.DeckWord.objects.create(deck=deck, word=second, position=1)
    card_models.DeckWord.objects.create(deck=deck, word=word, position=0)
    assert list(deck.deck_words.values_list("word_id", flat=True)) == [
        word.pk,
        second.pk,
    ]


@pytest.mark.parametrize("duplicate", ["word", "position"])
def test_duplicate_memberships_rejected(
    card_models: ModuleType,
    deck: Deck,
    duplicate: str,
):
    """A deck cannot repeat a word or assign two words the same position."""
    first = card_models.Word.objects.create(english="one", vietnamese="một")
    second = card_models.Word.objects.create(english="two", vietnamese="hai")
    card_models.DeckWord.objects.create(deck=deck, word=first, position=0)
    with transaction.atomic(), pytest.raises(IntegrityError):
        card_models.DeckWord.objects.create(
            deck=deck,
            word=first if duplicate == "word" else second,
            position=1 if duplicate == "word" else 0,
        )


def test_referenced_words_are_protected(
    card_models: ModuleType,
    deck: Deck,
    word: Word,
):
    """Words in a deck cannot be deleted accidentally."""
    card_models.DeckWord.objects.create(deck=deck, word=word, position=0)
    with pytest.raises(ProtectedError):
        word.delete()


@pytest.mark.parametrize("is_custom", [True, False])
def test_invalid_creator_combinations_rejected(
    card_models: ModuleType,
    learner: User,
    is_custom: bool,
):
    """Custom decks require a creator and starter decks must have none."""
    deck = card_models.Deck(
        title="Basics",
        level="A1",
        is_custom=is_custom,
        created_by=None if is_custom else learner,
    )
    with pytest.raises(ValidationError):
        deck.full_clean()
    with transaction.atomic(), pytest.raises(IntegrityError):
        deck.save()


def test_custom_creator_is_protected(card_models: ModuleType, learner: User):
    """Creators remain protected while they own decks."""
    deck = card_models.Deck(
        title="Custom",
        level="B1",
        is_custom=True,
        created_by=learner,
    )
    deck.full_clean()
    deck.save()
    with pytest.raises(ProtectedError):
        learner.delete()


def test_empty_deck_title_rejected(card_models: ModuleType):
    """Empty titles fail validation and direct writes."""
    deck = card_models.Deck(title="", level="A1")
    with pytest.raises(ValidationError):
        deck.full_clean()
    with transaction.atomic(), pytest.raises(IntegrityError):
        deck.save()


def test_deck_level_choices_validate_without_database_constraint():
    """Level choices are enforced by model validation only."""
    assert Deck.Level.values == ["A1", "A2", "B1", "B2", "C1", "C2"]
    deck = Deck(title="Basics", level=Deck.Level.A1)
    deck.full_clean()
    deck.level = "D1"
    with pytest.raises(ValidationError, match="level"):
        deck.full_clean()
    deck.save()
    deck.refresh_from_db()
    assert deck.level == "D1"


@pytest.mark.parametrize("field", ["english", "vietnamese"])
def test_required_word_text_rejected(card_models: ModuleType, field: str):
    """Both sides of a word must contain text."""
    word = card_models.Word(english="hello", vietnamese="xin chào")
    setattr(word, field, "")
    with pytest.raises(ValidationError):
        word.full_clean()
    with transaction.atomic(), pytest.raises(IntegrityError):
        word.save()


def test_independent_imports_allow_same_english(
    card_models: ModuleType,
    word: Word,
):
    """Equal English text preserves independent imported word identities."""
    imported = card_models.Word(english=word.english, vietnamese="chào")
    imported.full_clean()
    imported.save()
    assert imported.pk != word.pk


def test_negative_position_rejected(
    card_models: ModuleType,
    deck: Deck,
    word: Word,
):
    """Validation and database constraints reject negative positions."""
    membership = card_models.DeckWord(deck=deck, word=word, position=-1)
    with pytest.raises(ValidationError):
        membership.full_clean()
    with transaction.atomic(), pytest.raises(IntegrityError):
        membership.save()


@pytest.mark.parametrize("status", ["known", "review"])
def test_latest_word_grade(
    card_models: ModuleType,
    learner: User,
    word: Word,
    status: str,
):
    """Updating a grade replaces the previous value without another row."""
    progress, _ = card_models.WordProgress.objects.update_or_create(
        user=learner,
        word=word,
        defaults={"status": "review"},
    )
    updated, created = card_models.WordProgress.objects.update_or_create(
        user=learner,
        word=word,
        defaults={"status": status},
    )
    assert not created
    assert updated.pk == progress.pk
    assert updated.status == status


def test_invalid_progress_status(
    card_models: ModuleType,
    learner: User,
    word: Word,
):
    """Unsupported grades cannot enter the learning state."""
    progress = card_models.WordProgress(user=learner, word=word, status="new")
    with pytest.raises(ValidationError):
        progress.full_clean()
    with transaction.atomic(), pytest.raises(IntegrityError):
        progress.save()


@pytest.mark.parametrize("model_name", ["Bookmark", "UserLearningState"])
def test_unique_deck_learning_records(
    card_models: ModuleType,
    learner: User,
    deck: Deck,
    model_name: str,
):
    """Bookmarks and resume pointers cannot be duplicated for an account."""
    model = getattr(card_models, model_name)
    data = {"user": learner}
    data["deck" if model_name == "Bookmark" else "last_deck"] = deck
    model.objects.create(**data)
    with transaction.atomic(), pytest.raises(IntegrityError):
        model.objects.create(**data)


def test_unique_progress(card_models: ModuleType, learner: User, word: Word):
    """A word has only one grade per user, even across decks."""
    card_models.WordProgress.objects.create(
        user=learner,
        word=word,
        status="known",
    )
    with transaction.atomic(), pytest.raises(IntegrityError):
        card_models.WordProgress.objects.create(
            user=learner,
            word=word,
            status="review",
        )


def test_deleting_learner_cascades_learning_records(
    card_models: ModuleType,
    learner: User,
    word: Word,
    deck: Deck,
):
    """Account deletion clears learning data and preserves vocabulary."""
    card_models.WordProgress.objects.create(
        user=learner,
        word=word,
        status="known",
    )
    card_models.Bookmark.objects.create(user=learner, deck=deck)
    card_models.UserLearningState.objects.create(user=learner)
    learner.delete()
    assert not card_models.WordProgress.objects.exists()
    assert not card_models.Bookmark.objects.exists()
    assert not card_models.UserLearningState.objects.exists()
    assert card_models.Word.objects.filter(pk=word.pk).exists()
    assert card_models.Deck.objects.filter(pk=deck.pk).exists()


def test_unreferenced_word_cascades_progress(
    card_models: ModuleType,
    learner: User,
    word: Word,
):
    """Removing a word outside all decks removes obsolete progress."""
    card_models.WordProgress.objects.create(
        user=learner,
        word=word,
        status="known",
    )
    word.delete()
    assert not card_models.WordProgress.objects.exists()
