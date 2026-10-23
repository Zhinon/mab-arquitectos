document.querySelectorAll('.contact-form').forEach(form => {
  const button = form.querySelector('[type="submit"]');
  const label = button.querySelector('span');
  const status = form.querySelector('.form-status');
  const fields = [...form.querySelectorAll('[required]')];
  let sending = false;
  const setError = (field, message = '') => {
    field.setAttribute('aria-invalid', String(Boolean(message)));
    form.querySelector(`#${field.getAttribute('aria-describedby')}`).textContent = message;
  };
  const validate = field => {
    const message = field.validity.valueMissing || !field.value.trim()
      ? 'Completá este campo.'
      : field.validity.typeMismatch ? 'Revisá el formato del correo electrónico.' : '';
    setError(field, message);
    return !message;
  };
  fields.forEach(field => {
    field.addEventListener('blur', () => validate(field));
    field.addEventListener('input', () => {
      if (field.getAttribute('aria-invalid') === 'true') validate(field);
    });
  });
  // Native POST remains available when JavaScript is disabled.
  form.noValidate = true;
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (sending) return;
    const invalid = fields.filter(field => !validate(field));
    if (invalid.length) {
      status.textContent = 'Revisá los campos indicados antes de enviar.';
      invalid[0].focus();
      return;
    }
    sending = true;
    button.disabled = true;
    label.textContent = 'Enviando…';
    status.textContent = 'Estamos enviando tu consulta.';
    form.setAttribute('aria-busy', 'true');
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 25000);
    try {
      const response = await fetch(form.action, {
        method: 'POST', body: new FormData(form),
        headers: { Accept: 'application/json' }, signal: controller.signal
      });
      if (response.ok) {
        form.reset();
        fields.forEach(field => setError(field));
        status.textContent = '¡Gracias! Recibimos tu consulta. Te responderemos al correo que nos dejaste.';
      } else {
        const data = await response.json().catch(() => ({}));
        const invalidFields = [];
        (Array.isArray(data.errors) ? data.errors : []).forEach(error => {
          const field = fields.find(field => field.name === error.field);
          if (field) {
            setError(field, field.type === 'email' ? 'Revisá este correo o probá con otro.' : 'Revisá este campo antes de volver a enviar.');
            invalidFields.push(field);
          }
        });
        status.textContent = response.status === 429
          ? 'Hay demasiados intentos. Esperá unos minutos o escribinos por WhatsApp.'
          : invalidFields.length ? 'Revisá los campos indicados y volvé a enviar.'
          : 'No pudimos enviar tu consulta. Tus datos siguen acá: reintentá o escribinos por WhatsApp.';
        invalidFields[0]?.focus();
      }
    } catch (error) {
      status.textContent = error.name === 'AbortError'
        ? 'El envío demoró más de lo esperado. No pudimos confirmar la recepción; podés contactarnos por WhatsApp.'
        : 'No pudimos conectar para enviar. Revisá tu conexión y reintentá, o escribinos por WhatsApp.';
    } finally {
      clearTimeout(timeout);
      sending = false;
      button.disabled = false;
      label.textContent = 'Enviar consulta';
      form.removeAttribute('aria-busy');
    }
  });
});
