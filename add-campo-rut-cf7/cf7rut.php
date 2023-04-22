<?php
defined( 'ABSPATH' ) or die( 'No script kiddies please!' );


/**
 * ------------------------------------------------------------------------
 * Main class
 * ------------------------------------------------------------------------
 */

class CF7RUT {
    function __construct() {
        // Register shortcodes
        add_action('wpcf7_init', array(__CLASS__, 'add_shortcodes'));

        // Tag generator
        add_action('admin_init', array(__CLASS__, 'tag_generator'), 590);
    }

    static function add_shortcodes() {
        if (function_exists('wpcf7_add_form_tag'))
            wpcf7_add_form_tag(array( 'rut', 'rut*'), array(__CLASS__, 'shortcode_handler'), true);
        else if (function_exists('wpcf7_add_shortcode')) {
            wpcf7_add_shortcode(array( 'rut', 'rut*'), array(__CLASS__, 'shortcode_handler'), true);
        } else {
            throw new Exception('functions wpcf7_add_form_tag and wpcf7_add_shortcode not found.');
        }

        add_filter('wpcf7_messages', array(__CLASS__, 'wpcf7_text_messages_rut'), 30, 1 );
        add_filter('wpcf7_validate_rut', array(__CLASS__, 'validation_filter'), 10, 2);
        add_filter('wpcf7_validate_rut*', array(__CLASS__, 'validation_filter'), 10, 2);
    }


    static function shortcode_handler($tag) {
        if ( empty( $tag->name ) ) {
            return '';
        }
    
        $validation_error = wpcf7_get_validation_error( $tag->name );
    
        $class = wpcf7_form_controls_class( $tag->type, 'wpcf7-text' );
        $class .= ' wpcf7-validates-as-rut';
    
        if ( $validation_error ) {
            $class .= ' wpcf7-not-valid';
        }
    
        if( $tag->has_option( 'onformat' )){
            $class .= ' wpcf7-rut-onformat';
        }

        if( $tag->has_option( 'onlynumbers' )){
            $class .= ' wpcf7-rut-onlynumbers';
        }       

        $atts = array();
    
        $atts['size'] = $tag->get_size_option( '40' );
        $atts['maxlength'] = '9';
        $atts['minlength'] = $tag->get_minlength_option();
    
        if ( $atts['maxlength'] and $atts['minlength']
        and $atts['maxlength'] < $atts['minlength'] ) {
            unset( $atts['maxlength'], $atts['minlength'] );
        }
    
        $atts['class'] = $tag->get_class_option( $class );
        $atts['id'] = $tag->get_id_option();
        $atts['tabindex'] = $tag->get_option( 'tabindex', 'signed_int', true );
    
        if ( $tag->is_required() ) {
            $atts['aria-required'] = 'true';
        }
    
        $atts['aria-invalid'] = $validation_error ? 'true' : 'false';
    
        $value = (string) reset( $tag->values );
    
        if ( $tag->has_option( 'placeholder' )
        or $tag->has_option( 'watermark' ) ) {
            $atts['placeholder'] = $value;
            $value = '';
        }
    
        $value = $tag->get_default_option( $value );
    
        $value = wpcf7_get_hangover( $tag->name, $value );
    
        $atts['value'] = $value;
    
        if ( wpcf7_support_html5() ) {
            $atts['type'] = $tag->basetype;
        } else {
            $atts['type'] = 'text';
        }
    
        $atts['name'] = $tag->name;
    
        $atts = wpcf7_format_atts( $atts );

    
        $html = sprintf(
            '<span class="wpcf7-form-control-wrap %1$s"><input %2$s />%3$s</span>',
            sanitize_html_class( $tag->name ), $atts, $validation_error );
    
        return $html;    
    }


    static function tag_generator() {
        if (! function_exists( 'wpcf7_add_tag_generator'))
            return;

       wpcf7_add_tag_generator('rut',
            'RUT',
            'wpcf7-tg-pane-rut',
            array(__CLASS__, 'rut_pane')
        );

    }


    static function rut_pane( $contact_form, $args = '' ) {
    ?>
        <div class="control-box">
            <fieldset>
                <legend>Genera una etiqueta de formulario para un campo de entrada RUT. La validación del campo está contemplado por defecto.</legend>

                <table class="form-table">
                    <tbody>
                        <tr>
                        <th scope="row">Tipo de campo</th>
                        <td>
                            <fieldset>
                            <legend class="screen-reader-text">Tipo de campo</legend>
                            <label><input type="checkbox" name="required"> Campo requerido</label>
                            </fieldset>
                        </td>
                        </tr>

                        <tr>
                        <th scope="row"><label for="tag-generator-panel-text-name">Nombre</label></th>
                        <td><input type="text" name="name" class="tg-name oneline" id="tag-generator-panel-text-name"></td>
                        </tr>

                        <tr>
                        <th scope="row"><label for="tag-generator-panel-text-values">Valor predeterminado</label></th>
                        <td><input type="text" name="values" class="oneline" id="tag-generator-panel-text-values"><br>
                        <label><input type="checkbox" name="placeholder" class="option"> Use este texto como marcador del campo</label></td>
                        </tr>
                        <tr>
                        <th scope="row"><label for="tag-generator-panel-text-id">Atributo de ID</label></th>
                        <td><input type="text" name="id" class="idvalue oneline option" id="tag-generator-panel-text-id"></td>
                        </tr>

                        <tr>
                        <th scope="row"><label for="tag-generator-panel-text-class">Atributo de clase</label></th>
                        <td><input type="text" name="class" class="classvalue oneline option" id="tag-generator-panel-text-class"></td>
                        </tr>
                        <tr>
                        <th scope="row"><label for="tag-generator-panel-text-values">Auto formatear</label></th>
                        <td><label><input type="checkbox" name="onformat" class="option" checked="checked"> Permite automáticamente dar formato de RUT al campo</label></td>
                        </tr>
                        <tr>
                        <th scope="row"><label for="tag-generator-panel-text-values">Solo números</label></th>
                        <td><label><input type="checkbox" name="onlynumbers" class="option" checked="checked"> Solo permite ingresar números al campo</label></td>
                        </tr>                      
                    </tbody>
                </table>


            </fieldset>
        </div>

        <div class="insert-box">
            <input type="text" name="rut" class="tag code" readonly="readonly" onfocus="this.select()" />

            <div class="submitbox">
                <input type="button" class="button button-primary insert-tag" value="<?php echo esc_attr(__('Insert Tag', 'contact-form-7')); ?>" />
            </div>

            <br class="clear" />
            <p class="description mail-tag"><label for="tag-generator-panel-text-mailtag">Para recibir los datos enviados a través de este campo, debes insertar la etiqueta correspondiente (<strong><span class="mail-tag"></span></strong>) en alguno de los campos de la pestaña Correo electrónico.<input type="text" class="mail-tag code hidden" readonly="readonly" id="tag-generator-panel-text-mailtag"></label></p>
        </div>
    <?php
    }

    static function wpcf7_text_messages_rut( $messages ) {
        $messages = array_merge( $messages, array(
            'invalid_rut' => array(
                'description' => 'El RUT que introdujo el usuario no es válido',
                'default' => 'El RUT que has introducido no es válido.',
            ),
        ) );
        return $messages;
    }

    static function validation_filter($result, $tag) {
        
        $name = $tag->name;

        $value = isset( $_POST[$name] )
            ? trim( wp_unslash( strtr( (string) $_POST[$name], "\n", " " ) ) )
            : '';
    
        if ( 'rut' == $tag->basetype) {
            if( $tag->is_required() and '' == $value ) {
                $result->invalidate( $tag, wpcf7_get_message( 'invalid_required' ) );
            }elseif ('' != $value and !self::validate_rut($value)) {
                $result->invalidate( $tag, wpcf7_get_message( 'invalid_rut' ) );
            }
        }

        return $result;
    }


    static function validate_rut($rut){
        if (!preg_match("/^[0-9.]+[-]?+[0-9kK]{1}/", $rut)) {
            return false;
        }
        $rut = preg_replace('/[\.\-]/i', '', $rut);
        $dv = substr($rut, -1);
        $number = substr($rut, 0, strlen($rut) - 1);
        $i = 2;
        $sum = 0;
        foreach (array_reverse(str_split($number)) as $v) {
            if ($i == 8)
                $i = 2;
            $sum += $v * $i;
            ++$i;
        }
        $dvr = 11 - ($sum % 11);
        if ($dvr == 11)
            $dvr = 0;
        if ($dvr == 10)
            $dvr = 'K';
        if ($dvr == strtoupper($dv))
            return true;
        else
            return false;
    }

}

new CF7RUT;

/**
 * ------------------------------------------------------------------------
 * Get plugin url
 * ------------------------------------------------------------------------
 */

function wpcf7rf_plugin_url( $path = '' ) {
    $url = plugins_url( $path, WPCF7RF_PLUGIN );
    if ( is_ssl() && 'http:' == substr( $url, 0, 5 ) ) {
        $url = 'https:' . substr( $url, 5 );
    }
    return $url;
}

/**
 * ------------------------------------------------------------------------
 * Add required script
 * ------------------------------------------------------------------------
 */

add_action( 'wp_enqueue_scripts', 'wpcf7rf_enqueue_scripts', 20, 0 );
function wpcf7rf_enqueue_scripts() {
	wp_enqueue_script('wpcf7rf-scripts', wpcf7rf_plugin_url('scripts.js?'.time()), null, null, true);
}