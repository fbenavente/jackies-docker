=======max recursion deep
python manage.py test apps.api.tests.test_pre_checkout.PreCheckoutTestCase.test_pre_checkout_success
python manage.py test apps.shoppers.tests.test_checkout.FullShopperCheckoutTestCase.test_products_buy_unit_kg_cl
test_products_buy_unit_kg_mx - apps.shoppers.tests.test_checkout.FullShopperCheckoutTestCase
python manage.py test apps.api.tests.test_checkout.CheckoutTestCase.test_purcharse_with_debt
python manage.py test apps.api.tests.test_checkout.CheckoutTestCase.test_purchase
test_purchase_with_credits - apps.api.tests.test_checkout.CheckoutTestCase
test_purchase_with_products_cl - apps.api.tests.test_checkout.CheckoutTestCase
test_purchase_with_products_mx - apps.api.tests.test_checkout.CheckoutTestCase
test_purchase_with_single_product_unit_kg_cl - apps.api.tests.test_checkout.CheckoutTestCase
test_purchase_with_single_product_unit_kg_mx - apps.api.tests.test_checkout.CheckoutTestCase
=================
python manage.py test apps.city_management.tests.test_views.MultiplierCopyViewTestCase.test_post_correct
python manage.py test apps.city_management.tests.test_views.MultiplierCopyViewTestCase.test_post_date_another_zone_equal_date_in_future
Exception: [{'__all__': [u' is not a valid value']}, {'__all__': [u' is not a valid value']}]
test_post_overload_date - apps.city_management.tests.test_views.MultiplierCopyViewTestCase
test_post_overload_date_another_zone - apps.city_management.tests.test_views.MultiplierCopyViewTestCase
test_post_with_delete_and_invalid - apps.city_management.tests.test_views.MultiplierCopyViewTestCase


===revisando



python manage.py test apps.api.tests.test_checkout.CheckoutTestCase.test_purchase


 - 

 - 




test_redeemcode_for_non_buyers - apps.payments.tests.tests_integration.RedeemCodeIntegrationTest

test_resolve_task - apps.todo.tests.test_services.TaskService

test_send_subscription_expired_email - apps.subscriptions.tests.test_models.SubscriptionTerminationTestCase

test_set_order_requires_identification - apps.orders.tests.test_services.SetOrderRequiresIdentificationTestCase

test_set_store_status - apps.stores.tests.test_integrations.test_set_store_status.TestStoreStatus

test_set_store_status_without_permissions - apps.stores.tests.test_integrations.test_set_store_status.TestStoreStatus

test_shopper_no_booklog_entry - apps.customer_support.tests.test_handlers.CustomerSupportHandlersTest

test_shopper_workflow_all_refunds - apps.shoppers.tests.test_integration.ShopperCheckoutTestCase

test_shopper_workflow_integration - apps.shoppers.tests.test_integration.ShopperCheckoutTestCase

test_shopper_workflow_integration_on_a_different_branch - apps.shoppers.tests.test_integration.ShopperCheckoutTestCase

test_shopper_workflow_integration_order_v2 - apps.shoppers.tests.test_integration.ShopperCheckoutTestCase

test_single_branch - apps.checkout.tests.test_cart.CartValidationStepTestCase

test_single_order_delivery_pool_reject - apps.shoppers.tests.test_integration.ShopperCheckoutTestCase

test_slightly_greater_than_authorized_amount - apps.shoppers.tests.test_integration.ShopperCheckoutTestCase

test_stores - apps.api.tests.test_catalog.BranchTestCase

test_update_task - apps.todo.tests.test_services.TaskService

Ignacio Hermosilla