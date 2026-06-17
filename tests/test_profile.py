# tests/test_profile.py


TOAST_TEXT = "Profile saved"
TOAST_LIFETIME_MS = 18_000


# def test_profile_saved_notification_is_removed_after_18_seconds(
#     configured_page: Page,
#     base_url: str,
# ) -> None:
#     page = configured_page

#     initial_time = datetime.datetime(2026, 1, 1, 10, 0, 0, tzinfo=datetime.timezone.utc, )

#     page.clock.install(time=initial_time)
#     page.clock.pause_at(initial_time)

#     profile_page = ProfilePage(page, base_url)
#     profile = ProfileData(name="Oleg Voronch")

#     # GIVEN
#     profile_page.open()

#     # AND
#     profile_page.clear_name()

#     expect(
#         profile_page.name_input,
#         "Поле Name должно быть пустым после очистки",
#     ).to_have_value("")

#     expect(
#         profile_page.save_button,
#         "Кнопка Save должна быть отключена, пока обязательное поле Name пустое",
#     ).to_be_disabled()

#     # WHEN: пользователь вводит корректное имя.
#     profile_page.fill_profile(profile)

#     # THEN: введённое значение отображается в поле.
#     expect(
#         profile_page.name_input,
#         f"Поле Name должно содержать введённое значение: {profile.name!r}",
#     ).to_have_value(profile.name)

#     # AND: сохранение становится доступным.
#     expect(
#         profile_page.save_button,
#         "Кнопка Save должна стать доступной после заполнения обязательного поля Name",
#     ).to_be_enabled()

#     # WHEN: пользователь сохраняет профиль.
#     profile_page.save()

#     # THEN: появляется корректное уведомление.
#     expect(
#         profile_page.toast.root,
#         "После успешного сохранения должно появиться уведомление",
#     ).to_be_visible()

#     expect(
#         profile_page.toast.root,
#         f"Уведомление должно содержать текст {TOAST_TEXT!r}",
#     ).to_have_text(TOAST_TEXT)

#     # WHEN: прошло 17 999 миллисекунд.
#     page.clock.run_for(TOAST_LIFETIME_MS - 1)

#     # THEN: уведомление всё ещё отображается.
#     expect(
#         profile_page.toast.root,
#         "Уведомление не должно исчезнуть раньше установленных 18 секунд",
#     ).to_be_visible(timeout=1000)

#     # WHEN: наступает 18-я секунда.
#     page.clock.run_for(1)

#     # THEN: уведомление полностью удалено из DOM.
#     expect(
#         profile_page.toast.root,
#         "Уведомление должно быть удалено из DOM через 18 секунд",
#     ).to_have_count(0, timeout=1000)
