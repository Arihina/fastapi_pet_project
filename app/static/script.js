async function updateProductByStorekeeper() {
    const formData = new FormData(document.getElementById('updateProductForm'));

    const productData = {
    id: parseInt(formData.get('id')),
    price: formData.get('price') ? parseFloat(formData.get('price')) : null,
    count: formData.get('count') ? parseInt(formData.get('count')) : null,
    order_id: formData.get('order_id') ? parseInt(formData.get('order_id')) : null,
    description_id: formData.get('description_id') ? parseInt(formData.get('description_id')) : null,
    };

    try {
        const response = await fetch(`/storekeeper/products`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(productData),
        });

    } catch (error) {
        console.error('Ошибка обновления данных товара:', error);
        alert('Произошла ошибка при обновлении данных товара.');
    }
}
function goToProductsInfo() {
  window.location.href = "/storekeeper/products-info";
}
function goToSalesInfo() {
  window.location.href = "/storekeeper/sales-info";
}
function goToBuyersInfo() {
  window.location.href = "/storekeeper/buyers-info";
}
function goToOrdersInfo() {
  window.location.href = "/storekeeper/orders-info";
}
function goToOrderForm() {
  window.location.href = "/storekeeper/order-form";
}
function goToProductForm() {
  window.location.href = "/storekeeper/product-form";
}
function goToSaleForm() {
  window.location.href = "/storekeeper/sale-form";
}
function goToEditForm() {
  window.location.href = "/storekeeper/edit-form";
}
async function deleteSale(saleId) {
      if (!confirm("Вы уверены, что хотите удалить данные продажи?")) return;

      try {
        const response = await fetch(`/sales-accounting/${saleId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          const errorData = await response.json();
          const errorMessage = errorData.detail || `Error deleting buyer: ${response.status}`;
          alert(errorMessage);
          return;
        }

        location.reload();

      } catch (error) {
        console.error('Error:', error);
        alert('An unexpected error occurred.');
      }
}
async function submitFormSales() {
    const formData = new FormData(document.getElementById('saleForm'));
    const saleData = {};

    for (const [key, value] of formData.entries()) {
        saleData[key] = value;
    }

    try {
        const response = await fetch('/sales-accounting', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(saleData),
        });

        if (!response.ok) {
            let errorMessage = "Ошибка отправки формы";
            try {
                const errorData = await response.json();
                if (errorData.detail) {
                    errorMessage = errorData.detail;
                } else if (errorData.error){
                    errorMessage = errorData.error;
                }
            } catch (jsonError) {
                console.error("Ошибка парсинга ответа об ошибке:", jsonError);
                errorMessage = `Ошибка сервера: ${response.status}`;
            }
            alert(errorMessage);
            return;
        }

        alert('Продажа добавлен успешно!');
    } catch (error) {
        console.error('Ошибка отправки формы:', error);
        alert('Произошла ошибка при добавлении продажи.');
    }
}
async function updateSale(saleId) {
    const formData = new FormData(document.getElementById('updateSaleForm'));
    const saleData = {};
    for (const [key, value] of formData.entries()) {
        saleData[key] = value;
    }
    try {
        const response = await fetch(`/sales-accounting/${saleId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(saleData),
        });
        if (!response.ok) {
            let errorMessage = "Ошибка обновления данных продажи";
            try {
                const errorData = await response.json();
                if (errorData.detail) {
                    errorMessage = errorData.detail;
                } else if (errorData.error) {
                    errorMessage = errorData.error;
                }
            } catch (jsonError) {
                console.error("Ошибка парсинга ответа об ошибке:", jsonError);
                errorMessage = `Ошибка сервера: ${response.status}`;
            }
            alert(errorMessage);
            return;
        }
        alert('Данные продажи успешно обновлены!');
    } catch (error) {
        console.error('Ошибка обновления данных продажи:', error);
        alert('Произошла ошибка при обновлении данных продажи.');
    }
}
async function deleteProvider(providerId) {
      if (!confirm("Вы уверены, что хотите удалить поставщика?")) return;

      try {
        const response = await fetch(`/providers/${providerId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          const errorData = await response.json();
          const errorMessage = errorData.detail || `Error deleting buyer: ${response.status}`;
          alert(errorMessage);
          return;
        }

        location.reload();

      } catch (error) {
        console.error('Error:', error);
        alert('An unexpected error occurred.');
      }
}
async function submitFormProvider() {
    const formData = new FormData(document.getElementById('providerForm'));
    const providerData = {};

    for (const [key, value] of formData.entries()) {
        providerData[key] = value;
    }

    try {
        const response = await fetch('/providers', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(providerData),
        });

        if (!response.ok) {
            let errorMessage = "Ошибка отправки формы";
            try {
                const errorData = await response.json();
                if (errorData.detail) {
                    errorMessage = errorData.detail;
                } else if (errorData.error){
                    errorMessage = errorData.error;
                }
            } catch (jsonError) {
                console.error("Ошибка парсинга ответа об ошибке:", jsonError);
                errorMessage = `Ошибка сервера: ${response.status}`;
            }
            alert(errorMessage);
            return;
        }

        alert('Поставщик добавлен успешно!');
    } catch (error) {
        console.error('Ошибка отправки формы:', error);
        alert('Произошла ошибка при добавлении поставщика.');
    }
}
async function updateProvider(providerId) {
    const formData = new FormData(document.getElementById('updateProviderForm'));
    const providerData = {};
    for (const [key, value] of formData.entries()) {
        providerData[key] = value;
    }
    try {
        const response = await fetch(`/providers/${providerId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(providerData),
        });

        if (!response.ok) {
            let errorMessage = "Ошибка обновления данных поставщика";
            try {
                const errorData = await response.json();
                if (errorData.detail) {
                    errorMessage = errorData.detail;
                } else if (errorData.error) {
                    errorMessage = errorData.error;
                }
            } catch (jsonError) {
                console.error("Ошибка парсинга ответа об ошибке:", jsonError);
                errorMessage = `Ошибка сервера: ${response.status}`;
            }
            alert(errorMessage);
            return;
        }

        alert('Данные товара успешно обновлены!');
    } catch (error) {
        console.error('Ошибка обновления данных поставщика:', error);
        alert('Произошла ошибка при обновлении данных поставщика.');
    }
}
    async function deleteProduct(productId) {
      if (!confirm("Вы уверены, что хотите удалить товар?")) return;

      try {
        const response = await fetch(`/products/${productId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          const errorData = await response.json();
          const errorMessage = errorData.detail || `Error deleting buyer: ${response.status}`;
          alert(errorMessage);
          return;
        }

        location.reload();

      } catch (error) {
        console.error('Error:', error);
        alert('An unexpected error occurred.');
      }
    }
async function submitFormProduct() {
    const formData = new FormData(document.getElementById('productForm'));
    const productData = {};

    for (const [key, value] of formData.entries()) {
        productData[key] = value;
    }

    try {
        const response = await fetch('/products', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(productData),
        });

        if (!response.ok) {
            let errorMessage = "Ошибка отправки формы";
            try {
                const errorData = await response.json();
                if (errorData.detail) {
                    errorMessage = errorData.detail;
                } else if (errorData.error){
                    errorMessage = errorData.error;
                }
            } catch (jsonError) {
                console.error("Ошибка парсинга ответа об ошибке:", jsonError);
                errorMessage = `Ошибка сервера: ${response.status}`;
            }
            alert(errorMessage);
            return;
        }

        alert('Товар добавлен успешно!');
    } catch (error) {
        console.error('Ошибка отправки формы:', error);
        alert('Произошла ошибка при добавлении товара.');
    }
}
async function updateProduct(productId) {
    const formData = new FormData(document.getElementById('updateProductForm'));
    const productData = {};

    for (const [key, value] of formData.entries()) {
        productData[key] = value;
    }

    try {
        const response = await fetch(`/products/${productId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(productData),
        });

        if (!response.ok) {
            let errorMessage = "Ошибка обновления данных товара";
            try {
                const errorData = await response.json();
                if (errorData.detail) {
                    errorMessage = errorData.detail;
                } else if (errorData.error) {
                    errorMessage = errorData.error;
                }
            } catch (jsonError) {
                console.error("Ошибка парсинга ответа об ошибке:", jsonError);
                errorMessage = `Ошибка сервера: ${response.status}`;
            }
            alert(errorMessage);
            return;
        }

        alert('Данные товара успешно обновлены!');
    } catch (error) {
        console.error('Ошибка обновления данных товара:', error);
        alert('Произошла ошибка при обновлении данных товара.');
    }
}
async function submitFormOrder() {
    const formData = new FormData(document.getElementById('orderForm'));
    const orderData = {};

    for (const [key, value] of formData.entries()) {
        orderData[key] = value;
    }

    try {
        const response = await fetch('/orders', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(orderData),
        });

        if (!response.ok) {
            let errorMessage = "Ошибка отправки формы";
            try {
                const errorData = await response.json();
                if (errorData.detail) {
                    errorMessage = errorData.detail;
                } else if (errorData.error){
                    errorMessage = errorData.error;
                }
            } catch (jsonError) {
                console.error("Ошибка парсинга ответа об ошибке:", jsonError);
                errorMessage = `Ошибка сервера: ${response.status}`;
            }
            alert(errorMessage);
            return;
        }

        alert('Заказ добавлен успешно!');
    } catch (error) {
        console.error('Ошибка отправки формы:', error);
        alert('Произошла ошибка при добавлении заказа.');
    }
}
async function deleteOrder(orderId) {
      if (!confirm("Вы уверены, что хотите удалить заказ?")) return;

      try {
        const response = await fetch(`/orders/${orderId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          const errorData = await response.json();
          const errorMessage = errorData.detail || `Error deleting buyer: ${response.status}`;
          alert(errorMessage);
          return;
        }

        location.reload();

      } catch (error) {
        console.error('Error:', error);
        alert('An unexpected error occurred.');
      }
}
async function updateOrder(orderId) {
    const formData = new FormData(document.getElementById('updateOrderForm'));
    const orderData = {};

    for (const [key, value] of formData.entries()) {
        orderData[key] = value;
    }

    try {
        const response = await fetch(`/orders/${orderId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(orderData),
        });

        if (!response.ok) {
            let errorMessage = "Ошибка обновления данных заказа";
            try {
                const errorData = await response.json();
                if (errorData.detail) {
                    errorMessage = errorData.detail;
                } else if (errorData.error) {
                    errorMessage = errorData.error;
                }
            } catch (jsonError) {
                console.error("Ошибка парсинга ответа об ошибке:", jsonError);
                errorMessage = `Ошибка сервера: ${response.status}`;
            }
            alert(errorMessage);
            return;
        }

        alert('Данные заказа успешно обновлены!');
    } catch (error) {
        console.error('Ошибка обновления данных заказа:', error);
        alert('Произошла ошибка при обновлении данных заказа.');
    }
}
async function deleteDescription(descriptionId) {
      if (!confirm("Вы уверены, что хотите удалить описание?")) return;

      try {
        const response = await fetch(`/descriptions/${descriptionId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          const errorData = await response.json();
          const errorMessage = errorData.detail || `Error deleting buyer: ${response.status}`;
          alert(errorMessage);
          return;
        }

        location.reload();

      } catch (error) {
        console.error('Error:', error);
        alert('An unexpected error occurred.');
      }
    }
async function submitFormDescription() {
    const formData = new FormData(document.getElementById('descriptionForm'));
    const buyerData = {};

    for (const [key, value] of formData.entries()) {
        buyerData[key] = value;
    }

    try {
        const response = await fetch('/descriptions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(buyerData),
        });

        if (!response.ok) {
            let errorMessage = "Ошибка отправки формы";
            try {
                const errorData = await response.json();
                if (errorData.detail) {
                    errorMessage = errorData.detail;
                } else if (errorData.error){
                    errorMessage = errorData.error;
                }
            } catch (jsonError) {
                console.error("Ошибка парсинга ответа об ошибке:", jsonError);
                errorMessage = `Ошибка сервера: ${response.status}`;
            }
            alert(errorMessage);
            return;
        }

        alert('Описание добавлен успешно!');
    } catch (error) {
        console.error('Ошибка отправки формы:', error);
        alert('Произошла ошибка при добавлении описания.');
    }
}
async function updateDescription(dId) {
    const formData = new FormData(document.getElementById('updateDescrForm'));
    const descrData = {};

    for (const [key, value] of formData.entries()) {
        descrData[key] = value;
    }

    try {
        const response = await fetch(`/descriptions/${dId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(descrData),
        });

        if (!response.ok) {
            let errorMessage = "Ошибка обновления данных описания";
            try {
                const errorData = await response.json();
                if (errorData.detail) {
                    errorMessage = errorData.detail;
                } else if (errorData.error) {
                    errorMessage = errorData.error;
                }
            } catch (jsonError) {
                console.error("Ошибка парсинга ответа об ошибке:", jsonError);
                errorMessage = `Ошибка сервера: ${response.status}`;
            }
            alert(errorMessage);
            return;
        }

        alert('Данные описания успешно обновлены!');
    } catch (error) {
        console.error('Ошибка обновления данных описания:', error);
        alert('Произошла ошибка при обновлении данных описания.');
    }
}
async function deleteBuyer(buyerId) {
      if (!confirm("Вы уверены, что хотите удалить покупателя?")) return;

      try {
        const response = await fetch(`/buyers/${buyerId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          const errorData = await response.json();
          const errorMessage = errorData.detail || `Error deleting buyer: ${response.status}`;
          alert(errorMessage);
          return;
        }

        location.reload();

      } catch (error) {
        console.error('Error:', error);
        alert('An unexpected error occurred.');
      }
}
async function submitFormBuyer() {
    const formData = new FormData(document.getElementById('buyerForm'));
    const buyerData = {};

    for (const [key, value] of formData.entries()) {
        buyerData[key] = value;
    }

    try {
        const response = await fetch('/buyers', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(buyerData),
        });

        if (!response.ok) {
            let errorMessage = "Ошибка отправки формы";
            try {
                const errorData = await response.json();
                if (errorData.detail) {
                    errorMessage = errorData.detail;
                } else if (errorData.error){
                    errorMessage = errorData.error;
                }
            } catch (jsonError) {
                console.error("Ошибка парсинга ответа об ошибке:", jsonError);
                errorMessage = `Ошибка сервера: ${response.status}`;
            }
            alert(errorMessage);
            return;
        }

        alert('Покупатель добавлен успешно!');
    } catch (error) {
        console.error('Ошибка отправки формы:', error);
        alert('Произошла ошибка при добавлении покупателя.');
    }
}
async function updateBuyer(buyerId) {
    const formData = new FormData(document.getElementById('updateBuyerForm'));
    const buyerData = {};

    for (const [key, value] of formData.entries()) {
        buyerData[key] = value;
    }

    try {
        const response = await fetch(`/buyers/${buyerId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(buyerData),
        });

        if (!response.ok) {
            let errorMessage = "Ошибка обновления данных покупателя";
            try {
                const errorData = await response.json();
                if (errorData.detail) {
                    errorMessage = errorData.detail;
                } else if (errorData.error) {
                    errorMessage = errorData.error;
                }
            } catch (jsonError) {
                console.error("Ошибка парсинга ответа об ошибке:", jsonError);
                errorMessage = `Ошибка сервера: ${response.status}`;
            }
            alert(errorMessage);
            return;
        }

        alert('Данные покупателя успешно обновлены!');
    } catch (error) {
        console.error('Ошибка обновления данных покупателя:', error);
        alert('Произошла ошибка при обновлении данных покупателя.');
    }
}
function goToByers() {
  window.location.href = "/buyers";
}
function goToDescriptions() {
  window.location.href = "/descriptions";
}
function goToOrders() {
  window.location.href = "/orders";
}
function goToProviders() {
  window.location.href = "/providers";
}
function goToProducts() {
  window.location.href = "/products";
}
function goToSales() {
  window.location.href = "/sales-accounting";
}